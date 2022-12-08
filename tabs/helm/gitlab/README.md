# Gitlab Helm Chart Blueprint

## General

The blueprint installs Gitlab on top of Kubernetes cluster using the official Bitnami Helm chart.

## Requirements

In order to run successfully the blueprint you'll need an already running deployment of a Kubernetes cluster.
Then you have to set the `csys-obj-parent` label to the deployment ID of the Kubernetes cluster deployment.
In this way, all necessary credentials will be automatically passed to a Helm chart execution.

Example:
```shell
cfy install blueprint.yaml -b helm-gitlab -d helm-gitlab -l csys-obj-parent=K8S_DEPLOYMENT_ID
```

Using the GUI, `Deploy On` action can be used for that. It can be found under the `Bulk actions` button in the Deployments view. [Read more](https://docs.cloudify.co/latest/working_with/console/widgets/deploymentsview/#bulk-actions)

## Plugins0

cloudify-helm-plugin
cloudify-kubernetes-plugin

## Inputs

| Display Label                                                            | Name          | Type   | Default Value    |
| ------------------------------------------------------------------------ | ------------- | ------ | ---------------- |
| Email to be set in application                                           | issuer_email  | string | abc@cloudify.co  |
| Name of the helm release                                                 | release_name  | string | example          |
| Domain which will contain records to resolve gitlab, registry, and minio | domain        | string | abc.example.co   |
| Static IP that DNS record point to                                       | static_ip     | string | "10.10.10.10"    |

## Node Types

### Password Generator
the node type is responsible for generation of the password for Gitlab admin account.
The type is `cloudify.nodes.Root`.

### Helm install
the node type is responisble for installation of the helm binary in v3.7.2
The type is `cloudify.nodes.helm.Binary`. 

### Repo
the node type is responisble for downloading the Bitnami repository.
The type is `cloudify.nodes.helm.Repo`. 

### Release
the node type is responisble for installing the Gitlab deployment using the official Bitnami chart.
The type is `cloudify.nodes.helm.Release`. 

## Labels

The created deployment will have label `obj-type` equal to `helm`

## Capabilities

| Name            | Description                            |
| --------------- | -------------------------------------- |
| root_password   | the root password for the gitlab admin |
| gitlab_domain   | gitlab domain                          |
| gitlab_registry | gitlab registry domain                 |
| gitlab_minio    | gitlab minio domain                    |