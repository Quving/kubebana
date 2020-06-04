class Pod:
    def __init__(self, name, uuid, deployment, namespace, creation_timestamp):
        self.name = name
        self.uuid = uuid
        self.namespace = namespace
        self.deployment = deployment
        self.creation_timestamp = creation_timestamp

    @staticmethod
    def from_kubernetes_client(node_json):
        # Parse meta informations
        name = node_json.metadata.name
        uuid = node_json.metadata.uid
        namespace = node_json.metadata.namespace
        creation_timestamp = node_json.metadata.creation_timestamp

        deployment = "-".join(name.split("-")[:-2])
        return Pod(
            name=name,
            uuid=uuid,
            deployment=deployment,
            namespace=namespace,
            creation_timestamp=creation_timestamp,
        )

    def to_dict(self):
        attrs = {str(i): getattr(self, i) for i in dir(self) if
                 not i.startswith('__') and not callable(getattr(self, i))}
        return attrs
