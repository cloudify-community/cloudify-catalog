# Cert-Manager Helm Chart Blueprint

## General

The blueprint installs Cert-Manager on top of Kubernetes cluster using the official Bitnami Helm chart.

## Requirements

In order to run successfully the blueprint you'll need an already running deployment of a Kubernetes cluster.
Then you have to set the `csys-obj-parent` label to the deployment ID of the Kubernetes cluster deployment.
In this way, all necessary credentials will be automatically passed to a Helm chart execution.

Example:
```shell
cfy install blueprint.yaml -b helm-cert-manager -d helm-cert-manager -l csys-obj-parent=K8S_DEPLOYMENT_ID
```

Using the GUI, `Deploy On` action can be used for that. It can be found under the `Bulk actions` button in the Deployments view. [Read more](https://docs.cloudify.co/latest/working_with/console/widgets/deploymentsview/#bulk-actions)

## Plugins

cloudify-helm-plugin
cloudify-kubernetes-plugin

## Inputs

| Display Label                     | Name          | Type   | Default Value    |
| --------------------------------- | ------------- | ------ | ---------------- |
| Namespace to create resource      | namespace     | string | cert-manager     |
| Name of the helm release          | release_name  | string | example          |

## Node Types

### Namepsace
the node type is responsible for namespace creation. 
The type is `cloudify.kubernetes.resources.Namespace`.

### Helm install
the node type is responisble for installation of the helm binary in v3.7.2
The type is `cloudify.nodes.helm.Binary`. 

### Repo
the node type is responisble for downloading the Bitnami repository.
The type is `cloudify.nodes.helm.Repo`. 

### Release
the node type is responisble for installing the Wordpress deployment using the official Bitnami chart.
The type is `cloudify.nodes.helm.Release`. 

## Labels

The created deployment will have label `obj-type` equal to `helm`

## Capabilities

| Name          | Description                           |
| ------------- | ------------------------------------- |
| namespace     | Cert-manager service namespace        |
| service_name  | Cert-manager service name             |