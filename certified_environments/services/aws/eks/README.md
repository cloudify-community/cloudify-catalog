# EKS Service Provisioning

## General

The blueprint creates EKS service with one node that is accessible from the public network.

## Requirmennts

In order to run successfully the blueprint you'll need to provide the AWS environment - details [here](https://github.com/cloudify-community/eaas-example). 

## Secrets

The blueprint uses below secret in json format in order to set up service in AWS cloud - the example of the secret format could be found [here](https://github.com/cloudify-community/eaas-example/blob/master/secret.json).

| Name                  | Description                      |
| --------------------- | -------------------------------- |
| eeas_params           | The aks service configuration    |


## Plugins

* cloudify-aws-plugin
* cloudify-kubernetes-plugin

## Inputs

| Display Label                    | Name                | Type              | Default Value                                    |
| -------------------------------- | ------------------- | ----------------- | ------------------------------------------------ |
| Cloud Credentials from AWS env.  | cloud_credentials   | cloud_credentials | Please look at the cloud_credentials type legend |
| K8s configuration                | resource_config     | resource_config   | Please look at the resource_config type legend   |

### Custom types
cloud_credentials
| Property Name         | Type   | Default Value                       |
| --------------------- | ------ | ----------------------------------- |
| aws_access_key_id     | string | gets from cloud AWS env. capability |
| aws_keypair           | string | gets from cloud AWS env. capability |
| aws_secret_access_key | string | gets from cloud AWS env. capability |
| public_key_content    | string | gets from cloud AWS env. capability |
| private_key_content   | string | gets from cloud AWS env. capability |
| region_name           | string | gets from cloud AWS env. capability |


resource_config
| Property Name             | Type   | Default Value |
| ------------------------- | ------ | ------------- |
| kubernetes_version        | string | ''            |
| service_account_namespace | string | default       |


## Node Types

### Prefix
The node type is responsible to create a Prefix for the purpose of naming resources.\
The type is `eaas.nodes.UniquePrefixGenerator`.

For more details on the type can be found in the [link](https://github.com/cloudify-community/eaas-example/blob/master/utils/custom_types.yaml)

### Network
The node type is responsible for creating the network for EKS deployment.\
The type is `cloudify.nodes.ServiceComponent`.

### EKS Service IAM Role
The node type is responsible for setting up service permissions.\
The type is `cloudify.nodes.aws.iam.Role`.

### EKS Nodegroup IAM Role
The node type is responsible for setting up node group permissions.\
The type is `cloudify.nodes.aws.iam.Role`.

### EKS Cluster 
The node type is responsible for creating EKS cluster service.\
The type is `cloudify.nodes.aws.eks.Cluster`.

### EKS Node Group
The node type is responsible for adding the cluster to the specific node group.\
The type is `cloudify.nodes.aws.eks.NodeGroup`

### Kubernetes Master
The node type is responsible for setting up the cluster configuration.\
The type is `cloudify.kubernetes.nodes.Master`

### New Service Account
The node is responible for creating the new service account.\
The type is `cloudify.kubernetes.resources.ServiceAccount`.

### New Role Binding
The node is responsible for resource role binding for created service account.\
The type is `cloudify.kubernetes.resources.RoleBinding`

## Labels

The created deployment will have label `obj-type` equal to `service`