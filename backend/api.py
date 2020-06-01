from flask import request
from flask_api import FlaskAPI

from kubeapi import KubeApi

app = FlaskAPI(__name__)


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


if __name__ == "__main__":
    app.run(host='0.0.0.0')
