from flask import request
from flask_api import FlaskAPI, status
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

import util
from kubeapi import KubeApi

config = util.get_config()

app = FlaskAPI(__name__)
app.config['SECRET_KEY'] = config['secret_key']
CORS(app)

users = {}
for user in config['users']:
    users[user['username']] = generate_password_hash(user['password'])

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.route('/auth/', methods=['GET'])
@auth.login_required
def login():
    return {"status": "authorized"}


@app.route('/nodes/', methods=['GET'])
@auth.login_required
def list_nodes():
    label_selector = request.args.get('selector', default="", type=str)

    kubeapi = KubeApi()
    kubenodes = kubeapi.get_nodes(node_label_selector=label_selector)

    return [kubenode.to_dict() for kubenode in kubenodes]


@app.route('/deployments/', methods=['GET'])
@auth.login_required
def list_deployments():
    namespace_param = request.args.get('namespace', default="", type=str)

    kubeapi = KubeApi()
    deployments = []
    for namespace in namespace_param.split(","):
        deployments += kubeapi.get_deployments(namespace=namespace)
    return deployments


@app.route('/namespaces/', methods=['GET'])
@auth.login_required
def list_namespaces():
    kubeapi = KubeApi()
    return kubeapi.get_namespaces()


@app.route('/pods/', methods=['GET'])
@auth.login_required
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
@auth.login_required
def get_logs():
    namespace = request.args.get('namespace', default="", type=str)
    pod_name = request.args.get('pod_name', default="", type=str)
    session_id = request.args.get('session_id', default="", type=str)

    kubeapi = KubeApi()
    logs = kubeapi.get_logs_from_pod(pod_name, namespace)
    return {'session_id': session_id, 'log': logs}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
