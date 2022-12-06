# RDS PostgreSQL Service Provisioning

## General

The blueprint creates PostgreSQL service with masteruser name and password.

## Requirmennts

In order to run successfully the blueprint you'll need to provide the Azure environment - details [here](https://github.com/cloudify-community/eaas-example). 

## Secrets

The blueprint uses below secret in json format in order to set up service in Azure cloud - the example of the secret format could be found [here](https://github.com/cloudify-community/eaas-example/blob/master/secret.json).

| Name                  | Description                      |
| --------------------- | -------------------------------- |
| eeas_params           | The aks service configuration    |


## Plugins

cloudify-azure-plugin

## Inputs

| Display Label                            | Name                | Type              | Default Value                                            |
| ---------------------------------------- | ------------------- | ----------------- | -------------------------------------------------------- |
| Cloud Credentials from AWS env.          | cloud_credentials   | cloud_credentials | Please look at the cloud_credentials type legend         |
| Master username                          | resource_config     | resource_config   | The defualt value is fetched from the eeas_params secret |
| The resource prefix for resources naming | resource_prefix     | string            | ''                                                       |

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