from kubeapi import KubeApi

api = KubeApi()
print(api.get_pods(namespace="testing", deployment='ares-api')[0].to_dict())