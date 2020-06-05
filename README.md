# Kubebana

[![Build Status](https://drone.quving.com/api/badges/Quving/kubebana/status.svg)](https://drone.quving.com/Quving/kubebana)

## Motivation
Many companies use Kubernetes because Kubernetes now represents the industry standard.The framework is nowadays the backbone of every modern infrastructure of a tech company today. Kubernetes covers every imaginable function and everyone talks about it. However, Kubernetes is everything but not beginner-friendly due to its montrous complexity, even for DevOps. Kubernetes is not only a toy for Admins and DevOps. Developers who work in a tech company have to be familiar with Kubernetes as well. Sometimes a bug occurs in the application and the logs have to be analyzed. Depending on the [cloud provider](https://kubernetes.io/docs/concepts/cluster-administration/cloud-providers/) such as Azure, Aws, ... , developers have to authorize themselves differently, click through many non-trivial options and then access the logs. That's pain.


The other common way to access the logs is to use the [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/).  To get logs from a specific Pod, the command looks something like this.
```
kubectl logs -f ares-api-c4f94b944-dzbv8 -n testing
```

Except for the installation and setup of kubectl, the command is short and crisp, right? It is if you know the podname, whose postfix is usually generated by kubernetes, by memory. If not, you can start searching for the respective pod. For instance using the command to list all pods within the namespace:
```
kubectl get pods -n testing
```

In addition, the admin must be careful when giving a user the rights for kubectl. With kubectl the whole cluster can be managed. What if the developer is only allowed to have access to certain pods/deployment? Appropriate knowledge about the user administration of kubectl is required.

Well, you get the pain-point...


## Solution
Kubebana is a tool that solves this problem. It is characterized by the simplicity of accessing the logs of specific deployments or pods. It is a webapp and its use does not require a special setup (for the user/developer).


## Setup
### Environment Variables

web-service
 - KUBEBANA_API_HOST_PROTO (default: 'http')
 - KUBEBANA_API_HOST_PORT (default: '5000')
 - KUBEBANA_API_HOST (default: 'localhost')

server-service
 - None

### docker-compose.yml
```
services:
  server:
    image: quving/kubebana:server-master
    restart: always
    ports:
      - 5000:5000
    volumes:
      - ${HOME}/.kube/config:/root/.kube/config
    environment:
      - TZ=Europe/Berlin

  web:
    image: quving/kubebana:web-master
    ports:
      - 80:80
    depends_on:
      - server
    environment:
      - TZ=Europe/Berlin
      - KUBEBANA_API_HOST=server
```