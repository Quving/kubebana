from flask import request
from flask_api import FlaskAPI
from flask_cors import CORS

from kubeapi import KubeApi

app = FlaskAPI(__name__)
CORS(app)


@app.route('/nodes/', methods=['GET'])
def list_nodes():
    label_selector = request.args.get('selector', default="", type=str)

    kubeapi = KubeApi()
    kubenodes = kubeapi.get_nodes(node_label_selector=label_selector)

    return [kubenode.to_dict() for kubenode in kubenodes]


@app.route('/deployments/', methods=['GET'])
def list_deployments():
    namespace_param = request.args.get('namespace', default="", type=str)

    kubeapi = KubeApi()
    deployments = []
    for namespace in namespace_param.split(","):
        deployments += kubeapi.get_deployments(namespace=namespace)
    return deployments


@app.route('/namespaces/', methods=['GET'])
def list_namespaces():
    kubeapi = KubeApi()
    return kubeapi.get_namespaces()


@app.route('/pods/', methods=['GET'])
def list_pods():
    namespace_param = request.args.get('namespace', default="", type=str)
    deployment_param = request.args.get('deployment', default="", type=str)

    kubeapi = KubeApi()
    pods = []
    for deployment in deployment_param.split(","):
        for namespace in namespace_param.split(","):
            pods += kubeapi.get_pods(namespace, deployment)

    return [pod.to_dict() for pod in pods]


@app.route('/logs/', methods=['GET'])
def get_logs():
    namespace = request.args.get('namespace', default="", type=str)
    pod_name = request.args.get('pod_name', default="", type=str)
    session_id = request.args.get('session_id', default="", type=str)

    kubeapi = KubeApi()
    logs = kubeapi.get_logs_from_pod(pod_name, namespace)
    return {'session_id': session_id, 'log': logs}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
