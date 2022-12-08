# MongoDB Helm Chart Blueprint

## General

The blueprint installs MongoDB on top of Kubernetes cluster using the official Bitnami Helm chart.

## Requirements

In order to run successfully the blueprint you'll need an already running deployment of a Kubernetes cluster.
Then you have to set the `csys-obj-parent` label to the deployment ID of the Kubernetes cluster deployment.
In this way, all necessary credentials will be automatically passed to a Helm chart execution.

Example:
```shell
cfy install blueprint.yaml -b helm-mongo -d helm-mongo -l csys-obj-parent=K8S_DEPLOYMENT_ID
```

Using the GUI, `Deploy On` action can be used for that. It can be found under the `Bulk actions` button in the Deployments view. [Read more](https://docs.cloudify.co/latest/working_with/console/widgets/deploymentsview/#bulk-actions)


Example usage: 
```shell
sudo apt install mongodb-clients -y
mongo --host 34.82.43.207 --port 27017 -u root --password --authenticationDatabase "admin"
```

## Plugins

cloudify-helm-plugin
cloudify-kubernetes-plugin

## Inputs

| Display Label                     | Name          | Type   | Default Value    |
| --------------------------------- | ------------- | ------ | ---------------- |
| Number of pod replicas            | replica_count | string | "1"              |
| Name of the helm release          | release_name  | string | exampleMongoDB   |

## Node Types

### Password Generator
the node type is responsible for password generation for the root MongoDB user
The type is `cloudify.nodes.helm.Release` 

### Helm install
the node type is responisble for installation of the helm binary in v3.7.2
The type is `cloudify.nodes.helm.Binary`. 

### Repo
the node type is responsible for downloading the Bitnami repository.
The type is `cloudify.nodes.helm.Repo`. 

### Release
the node type is responsible for installing the MongoDB deployment using the official Bitnami chart.
The type is `cloudify.nodes.helm.Release`. 

### Svc
the node type is responsible for getting the details of the running service. It's used in capabilities for exposing the URLs.
The type is `cloudify.kubernetes.resources.Service`.

## Labels

The created deployment will have label `obj-type` equal to `helm`

## Capabilities

| Name          | Description                  |
| ------------- | ---------------------------- |
| root_password | Password for the root user   |
| mongodb_ip    | MongoDB server IP            |
| port          | MongoDB port                 |