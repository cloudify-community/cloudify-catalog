# GCP MariaDB Provisioning

## General

The blueprint creates GCP Cloud MariaDB instance.

## Requirements

In order to run successfully the blueprint you'll need Google Credentials file in JSON format. The credentials to the Google cloud should have permission to describe, update, delete and create network service.

## Secrets

The blueprint uses secrets in order to connect to GCP cloud so you need to connfigure them prior running the blueprint.


| Name            | Description                        |
| --------------- | ---------------------------------- |
| gcp_credentials | Google Credentials in JSON format  |

## Plugins


cloudify-terraform-plugin

## Inputs

| Display Label                            | Name                | Type   | Default Value |
| ---------------------------------------- | ------------------- | ------ | ------------- |
| The resource prefix for resources naming | resource_prefix     | string | ''            |
| Google region name                       | region_name         | string | us-west1      |

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

The created deployment will have label `obj-type` equal to `service`, `gcp` & `mariadb`