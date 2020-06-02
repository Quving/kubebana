from flask import request
from flask_api import FlaskAPI

from kubeapi import KubeApi
from flask_cors import CORS

app = FlaskAPI(__name__)
CORS(app)

@app.route('/nodes/', methods=['GET'])
def list_nodes():
    label_selector = request.args.get('selector', default=None, type=str)

    kubeapi = KubeApi()
    kubenodes = kubeapi.get_nodes(node_label_selector=label_selector)

    return [kubenode.to_dict() for kubenode in kubenodes]


@app.route('/deployments/', methods=['GET'])
def list_deployments():
    namespace = request.args.get('namespace', default=None, type=str)

    kubeapi = KubeApi()
    return kubeapi.get_deployments(namespace=namespace)


@app.route('/pods/', methods=['GET'])
def get_pods():
    namespace = request.args.get('namespace', default=None, type=str)
    deployment = request.args.get('deployment', default=None, type=str)

    kubeapi = KubeApi()
    pods = kubeapi.get_pods(namespace, deployment)
    return [pod.to_dict() for pod in pods]


@app.route('/logs/', methods=['GET'])
def get_logs():
    namespace = request.args.get('namespace', default=None, type=str)
    pod_name = request.args.get('pod_name', default=None, type=str)
    session_id = request.args.get('session_id', default=None, type=str)

    kubeapi = KubeApi()
    logs = kubeapi.get_logs_from_pod(pod_name, namespace)
    return {'session_id': session_id, 'log': logs}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
