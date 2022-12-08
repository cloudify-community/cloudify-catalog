# Redis Helm Chart Blueprint

## General

The blueprint installs Redis on top of Kubernetes cluster using the official Bitnami Helm chart.

Example usage:
``` shell
redic-cli -h <redis_endpoint> -a <redis_password>
```

## Requirements

In order to run successfully the blueprint you'll need an already running deployment of a Kubernetes cluster.
Then you have to set the `csys-obj-parent` label to the deployment ID of the Kubernetes cluster deployment.
In this way, all necessary credentials will be automatically passed to a Helm chart execution.

Example:
```shell
cfy install blueprint.yaml -b helm-redis -d helm-redis -l csys-obj-parent=K8S_DEPLOYMENT_ID
```

Using the GUI, `Deploy On` action can be used for that. It can be found under the `Bulk actions` button in the Deployments view. [Read more](https://docs.cloudify.co/latest/working_with/console/widgets/deploymentsview/#bulk-actions)

## Plugins

cloudify-helm-plugin
cloudify-kubernetes-plugin

## Inputs

| Display Label                     | Name          | Type   | Default Value    |
| --------------------------------- | ------------- | ------ | ---------------- |
| Name of the helm release          | release_name  | string | example          |

## Node Types

### Password generator
the node type is reponsible for generation of random password to access Redis 
The type is `cloudify.nodes.Root`

### Helm install
the node type is responisble for installation of the helm binary in v3.7.2
The type is `cloudify.nodes.helm.Binary`. 

### Repo
the node type is responisble for downloading the Bitnami repository.
The type is `cloudify.nodes.helm.Repo`. 

### Release
the node type is responisble for installing the Redis deployment using the official Bitnami chart.
The type is `cloudify.nodes.helm.Release`. 

### Svc
the node type is responisble for getting the details of the running service. It's used in capabilities for exposing the URLs.
The type is `cloudify.kubernetes.resources.Service`.

## Labels

The created deployment will have label `obj-type` equal to `helm`

## Capabilities

| Name           | Description                              |
| -------------- | ---------------------------------------- |
| redis_endpoint | ip for the redis connection              |
| redis_password | password for the redis server connection |