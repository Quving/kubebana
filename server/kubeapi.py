import json
import time

from kubernetes import client, config
from kubernetes.client.rest import ApiException

from models.node import Node
from models.pod import Pod
from util import Logger


class KubeApi:
    def __init__(self):
        config.load_kube_config()
        self.logger = Logger.logger

    def get_logs_from_pod(self, pod_name, namespace, retry_timer=5):
        """
        Get the log of a single pod.py.
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
                error_dict = json.loads(e.body)
                self.logger.error("{}: {}".format(error_dict['status'], error_dict['message']))
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

                kubenodes = [Node.from_kubernetes_client(node_json=node) for node in ret.items]
                kubenodes = sorted(kubenodes, key=lambda k: k.name)

                return kubenodes
            except ApiException as e:
                error_dict = json.loads(e.body)
                self.logger.error("{}: {}".format(error_dict['status'], error_dict['message']))
                time.sleep(retry_timer)

    def get_pods(self, namespace, deployment, retry_timer=5):
        """
        Returns a list of pods for a specific deployment within a specifc namespace.
        """
        while True:
            try:
                api_client = client.CoreV1Api()
                field_selector = 'metadata.namespace=' + namespace
                res = api_client.list_pod_for_all_namespaces(field_selector=field_selector)
                pods = [Pod.from_kubernetes_client(r) for r in res.items]

                return [pod for pod in pods if pod.deployment == deployment]
            except ApiException as e:
                error_dict = json.loads(e.body)
                self.logger.error("{}: {}".format(error_dict['status'], error_dict['message']))
                time.sleep(retry_timer)

    def get_deployments(self, namespace, retry_timer=5):
        """
        Returns a list of deployment names in a given namespace.
        """
        while True:
            try:
                api_client = client.AppsV1Api()
                res = [r.metadata.name for r in api_client.list_namespaced_deployment(namespace=namespace).items]

                return res
            except ApiException as e:
                error_dict = json.loads(e.body)
                self.logger.error("{}: {}".format(error_dict['status'], error_dict['message']))
                time.sleep(retry_timer)
