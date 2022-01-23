# RDS PostgreSQL Service Provisioning

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

cloudify-aws-plugin

## Inputs

| Display Label                      | Name                | Type              | Default Value                                              |
| ---------------------------------- | ------------------- | ----------------- | ---------------------------------------------------------- |
| Cloud Credentials from AWS env.    | cloud_credentials   | cloud_credentials | (The secrets values from AWS environment)                  |
| K8s vers. & srv. account namespace | resource_config     | resource_config   | kubernetes_version: '', service_account_namespace: defualt |

## Node Types

### Prefix
The node type is responsible to create a Prefix for the purpose of naming resources.
The type is `eaas.nodes.UniquePrefixGenerator`.

For more details on the type can be found in the [link](https://github.com/cloudify-community/eaas-example/blob/master/utils/custom_types.yaml)

### Network
The node type is responsible for creating the network for EKS deployment. 
The type is `cloudify.nodes.ServiceComponent`.

### Database stack
The node type is responsible for configuration of the database stack such as Security group, subnet & database master username/password. 
The type is `cloudify.nodes.aws.CloudFormation.Stack`

## Labels

The created deployment will have label `obj-type` equal to `service`