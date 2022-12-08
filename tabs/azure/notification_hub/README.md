# Notification Hub Service Provisioning

## General

The blueprint creates Notification Hub service with the usage of the ARM template - details [here](https://docs.microsoft.com/en-us/azure/notification-hubs/create-notification-hub-template?tabs=PowerShell). 

## Requirements

Install sercrets and plugins listed below, no specific requriements needed. 

## Secrets

The blueprint uses below secret in json format in order to set up service in Azure cloud.

| Name                  | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| azure_tenant_id       | Azure tenant ID                                                                    |
| azure_subscription_id | Azure subcription ID                                                               |
| azure_client_id       | Azure client ID                                                                    |
| azure_client_secret   | Azure client secret                                                                |


## Plugins

cloudify-terraform-plugin
cloudify-azure-plugin


## Inputs

| Display Label                            | Name               | Type   | Default Value  |
| ---------------------------------------- | ------------------ | ------ | -------------- |
| The resource prefix for resources naming | resource_prefix    | string | ''             |
| Azure region name                        | azure_region_name  | string | EastUs         |

If the user provides empty value of default the prefix will be gerenated automatically.


## Node Types

### Prefix
The node type is responsible to create a Prefix for the purpose of naming resources.\
The type is `eaas.nodes.UniquePrefixGenerator`.

For more details on the type can be found in the [link](https://github.com/cloudify-community/eaas-example/blob/master/utils/custom_types.yaml)

### Terraform
The node type is responsible for configuration the host for terraform.\
The type is `cloudify.nodes.terraform`.

### Terraform Module
The node type responsible for deploying the terraform code.\
Derived type is `cloudify.nodes.terraform.Module`.

### Notification Hub Deployment
The node type is responsible for deploying the Notification Hub in the Azure cloud.\
Derived type is `cloudify.azure.Deployment`.


## Labels

The created deployment will have label `obj-type` equal to `service`