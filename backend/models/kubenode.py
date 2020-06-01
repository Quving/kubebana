import json


class KubeNode:
    def __init__(self, name, uid, memory_pressure, disk_pressure, pid_pressure, ready):
        self.name = name
        self.uid = uid
        self.memory_pressure = memory_pressure
        self.disk_pressure = disk_pressure
        self.pid_pressure = pid_pressure
        self.ready = ready

    @staticmethod
    def from_kubernetes_client(node_json):
        # Parse meta informations
        name = node_json.metadata.name
        uid = node_json.metadata.uid

        # Parse node conditions
        for condition_json in node_json.status.conditions:
            type = condition_json.type
            if type == 'MemoryPressure':
                memory_pressure = condition_json.status == 'True'

            if type == 'DiskPressure':
                disk_pressure = condition_json.status == 'True'

            if type == 'PIDPressure':
                pid_pressure = condition_json.status == 'True'

            if type == 'Ready':
                ready = condition_json.status == 'True'

        return KubeNode(
            name=name,
            uid=uid,
            memory_pressure=memory_pressure,
            disk_pressure=disk_pressure,
            pid_pressure=pid_pressure,
            ready=ready
        )

    @staticmethod
    def from_dict(kubenode_json):
        return KubeNode(
            name=kubenode_json['name'],
            uid=kubenode_json['uid'],
            memory_pressure=kubenode_json['memory_pressure'],
            disk_pressure=kubenode_json['disk_pressure'],
            pid_pressure=kubenode_json['pid_pressure'],
            ready=kubenode_json['ready']
        )

    def to_dict(self):
        attrs = {str(i): getattr(self, i) for i in dir(self) if
                 not i.startswith('__') and not callable(getattr(self, i))}
        return attrs

    def __str__(self):
        attrs = {str(i): getattr(self, i) for i in dir(self) if not i.startswith('__')}
        return json.dumps(attrs)
