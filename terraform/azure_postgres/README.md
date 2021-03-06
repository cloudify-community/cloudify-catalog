# PostgreSQL Service Provisioning

## General

The blueprint creates PostgreSQL service on the Azure cloud.

## Requirements

In order to run successfully the blueprint you'll need Azure subscription id, tenant id, client id and client secret. The credentials to the Azure should have permission to describe, update, delete and create PostgreSQL flexible database service.

## Secrets

The blueprint uses secrets to connect to cloud, you need to connfigure them prior running the blueprint.


| Name                  | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| azure_tenant_id       | Azure tenant ID                                                                    |
| azure_subscription_id | Azure subcription ID                                                               |
| azure_client_id       | Azure client ID                                                                    |
| azure_client_secret   | Azure client secret                                                                |

## Plugins

cloudify-terraform-plugin

## Inputs

| Display Label                            | Name            | Type   | Default Value  |
| ---------------------------------------- | ----------------| ------ | -------------- |
| The resource prefix for resources naming | resource_prefix | string | ''             |
| Azure location name                      | region          | string | EastUS         |
| The password for database user           | password        | string | 

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
Derived type is `cloudify.nodes.terraform.Module`

## Labels

The created deployment will have label `obj-type` equal to `service`