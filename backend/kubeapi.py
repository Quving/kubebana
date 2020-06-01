import json
import os
import random
import subprocess
import time
from pprint import pprint

from kubernetes import client, config
from kubernetes.client.rest import ApiException

from models.kubenode import KubeNode
from util import Logger


class KubeApi:
    def __init__(self):
        config.load_kube_config()
        self.logger = Logger.logger

    def get_logs_from_pod(self, pod_name, namespace, retry_timer=5):
        """
        Get the log of a single pod.
        """
        while True:
            try:
                api_client = client.CoreV1Api()
                ret = api_client.read_namespaced_pod_log(
                    name=pod_name,
                    namespace=namespace,
                    pretty=True,
                )
                return ret

            except ApiException as e:
                error_dict = json.loads(e.body)
                self.logger.error("{}: {}".format(error_dict['status'], error_dict['message']))
                time.sleep(retry_timer)

    def get_namespaces(self, retry_timer=5):
        """
        List namespaces within the kubernetes cluster.
        """
        while True:
            try:
                api_client = client.CoreV1Api()
                ret = api_client.list_namespace()
                return [n.metadata.name for n in ret.items]

            except ApiException as e:
                self.logger.error("KubeApi is currently not available (503). Request will be retried in 5s.")
                time.sleep(retry_timer)

    def get_nodes(self, node_label_selector, retry_timer=5):
        """
        Returns a list of KubeNodes that is matched to the label selector.
        """
        while True:
            try:
                api_client = client.CoreV1Api()
                if node_label_selector:
                    ret = api_client.list_node(label_selector=node_label_selector)
                else:
                    ret = api_client.list_node()

                kubenodes = [KubeNode.from_kubernetes_client(node_json=node) for node in ret.items]
                kubenodes = sorted(kubenodes, key=lambda k: k.name)

                return kubenodes
            except ApiException as e:
                self.logger.error("KubeApi is currently not available (503). Request will be retried in 5s.")
                time.sleep(retry_timer)

    def get_deployments(self, namespace, retry_timer=5):
        """
        Returns a list of deployment names within a specified namespace.
        """
        while True:
            try:
                api_client = client.AppsV1Api()
                res = api_client.list_namespaced_deployment(namespace=namespace)
                return [r.metadata.name for r in res.items]
            except ApiException as e:
                self.logger.error("KubeApi is currently not available (503). Request will be retried in 5s.")
                time.sleep(retry_timer)

    def watch_rollout(self, deployment_name, namespace, timeout=180, verbose=False):
        """
        Start Kubebalancer watching thread.
        """
        api = client.AppsV1Api()
        start = time.time()
        msg = ''
        while time.time() - start < timeout:
            time.sleep(2)
            response = api.read_namespaced_deployment_status(deployment_name, namespace)
            s = response.status
            if (s.updated_replicas == response.spec.replicas and
                    s.replicas == response.spec.replicas and
                    s.available_replicas == response.spec.replicas and
                    s.observed_generation >= response.metadata.generation):
                return True
            else:
                msg_new = '[updated_replicas: {}, replicas: {}, available_replicas: {}, observed_generation: {}]' \
                    .format(s.updated_replicas, s.replicas - 1, s.available_replicas, s.observed_generation)
                if not msg == msg_new and verbose:
                    print(msg_new)
                    msg = msg_new

        raise RuntimeError('Waiting timeout for deployment {}'.format(deployment_name))

    def execute_shell_cmd(self, cmd_str):
        """
        Execute a given cmd on the shell, attaches the output and returns the exit value.
        """
        process = subprocess.Popen(cmd_str.split(), stdout=subprocess.PIPE, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            print(output.strip())
            return_code = process.poll()
            if return_code is not None:
                return return_code

    def restart_rollout(self, deployment_name, namespace):
        """
        Restart a kubernetes rollout.
        """
        command = 'kubectl rollout restart deployment/{} -n {}'.format(deployment_name, namespace)
        self.execute_shell_cmd(command)

    def watch_health(self, namespace, deployments, node_label_selector, interval=5):
        # Settings
        filename = 'healthy_state.json'

        self.logger.info('The health will be checked in an interval of {} seconds.'.format(interval))

        def save_kubenode_states_to_file(kubenodes):
            with open(filename, 'w') as file:
                json_dicts = [kn.to_dict() for kn in kubenodes]
                json.dump(json_dicts, file, indent=4)
            return kubenodes

        def load_kubenode_states_from_file():
            with open(filename, 'r') as file:
                return [KubeNode.from_dict(json) for json in json.load(file)]

        # Check if a initial kubenodes atate has been set.
        if os.path.exists(filename):
            kubenode_states = load_kubenode_states_from_file()
            self.logger.info(
                'Preset kubenode states found. {} kubenode(s) are set as healthy state.\n'.format(len(kubenode_states)))
        else:
            kubenode_states = self.get_nodes(node_label_selector)
            self.logger.info(
                'No preset kubenode states found. Current state of will be set as healty state. {} kubenode(s) found.\n'
                    .format(len(kubenode_states)))
            save_kubenode_states_to_file(kubenode_states)

        pprint([n.to_dict() for n in kubenode_states])
        print('\n')

        self.logger.info('Start monitoring kubenodes.')
        while True:
            time.sleep(interval)
            kubenode_state_now = self.get_nodes(node_label_selector)

            n_nodes_ready_before = len([n for n in kubenode_states if n.ready])
            n_nodes_ready_now = len([n for n in kubenode_state_now if n.ready])

            # Detect if a node came only recently (since last check interval).
            diff = n_nodes_ready_before - n_nodes_ready_now
            if diff < 0:
                self.logger.info("{} node(s) came online since last check.".format(abs(diff)))

                # Check if no deployments are specified, deploy random n+dp/m_nodes deployments.
                if not deployments:
                    self.logger.info("No deployments specified. Automatic rescheduling will be applied.")
                    n_dp_to_restart = int(len(self.get_deployments(namespace=namespace)) / n_nodes_ready_now)
                    self.logger.info("{} random selected deployments will be rescheduled.".format(n_dp_to_restart))
                    deployments = random.sample(self.get_deployments(namespace), k=n_dp_to_restart)

                for deployment in deployments:
                    self.logger.info("Deployment \"{}\" will be rescheduled.".format(deployment))
                    self.restart_rollout(namespace=namespace, deployment_name=deployment)
                    self.watch_rollout(namespace=namespace, deployment_name=deployment)

                self.logger.info("Rescheduling process applied.")


            # Nothing is happening. Same state as before.
            elif diff == 0:
                pass

            # Greater than equals 1: Node went offline since last check.
            else:
                self.logger.info("{} node(s) went offline since last check.".format(abs(diff)))
                pass

            kubenode_states = kubenode_state_now
