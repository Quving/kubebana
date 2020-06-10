from flask import request
from flask_api import FlaskAPI
from flask_cors import CORS
from flask_jwt import JWT, jwt_required
from werkzeug.security import safe_str_cmp

import util
from kubeapi import KubeApi


class User(object):
    def __init__(self, id, username, password):
        self.id = id,
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


config = util.get_config()

users = []
for i in range(len(config['users'])):
    users.append(User(i, config['users'][i]['username'], config['users'][i]['password']))
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app = FlaskAPI(__name__)
app.config['SECRET_KEY'] = config['secret_key']
CORS(app)

jwt = JWT(app, authenticate, identity)


@jwt_required()
@app.route('/nodes/', methods=['GET'])
def list_nodes():
    label_selector = request.args.get('selector', default="", type=str)

    kubeapi = KubeApi()
    kubenodes = kubeapi.get_nodes(node_label_selector=label_selector)

    return [kubenode.to_dict() for kubenode in kubenodes]


@jwt_required()
@app.route('/deployments/', methods=['GET'])
def list_deployments():
    namespace_param = request.args.get('namespace', default="", type=str)

    kubeapi = KubeApi()
    deployments = []
    for namespace in namespace_param.split(","):
        deployments += kubeapi.get_deployments(namespace=namespace)
    return deployments


@jwt_required()
@app.route('/namespaces/', methods=['GET'])
def list_namespaces():
    kubeapi = KubeApi()
    return kubeapi.get_namespaces()


@jwt_required()
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


@jwt_required()
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
