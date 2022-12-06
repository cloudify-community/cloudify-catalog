# Tflint Usage Example

## General

The blueprint depicts how to use [TFlint](https://github.com/terraform-linters/tflint) - framework that Cloudify uses to provide static code analysis. It’s made to enforce best practices, check naming conventions, and warn about possible errors with major Cloud providers.
 

## Requirements

In order to run successfully the blueprint you'll need AWS access key id and AWS secret access key. The credentials to the AWS should have permission to describe, update, delete and create AWS resources.

## Secrets

The blueprint uses secrets to connect to cloud, you need to connfigure them prior running the blueprint.


| Name                  | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| aws_access_key_id     | AWS Access Key ID                                                                  |
| aws_aceess_secret_key | AWS Access Secret Key                                                              |

## Plugins

cloudify-terraform-plugin\
cloudify-utilities-plugin


## Inputs

| Display Label                                  | Name   | Type         | Default Value |
| ------------------------- | ------------------ | ------ | --------------- |
| AWS region name           | aws_region_name    | string | ''            |
| Module source URL         | module_source      | string | https://github.com/cloudify-community/tf-source/archive/refs/heads/main.zip    |
| Module to deploy path     | module_source_path | string | 'template/modules/public_vm/' | 



If the user provides empty value of default the prefix will be gerenated automatically.


## Node Types

### Key
The node type is responsible for create SSH key pair for deployment.\
The type is `cloudify.keys.nodes.RSAKey`.

### Terraform
The node type is responsible for configuration the host for terraform.\
The type is `cloudify.nodes.terraform`.

### Terraform Module
The node type responsible for deploying the terraform code.\
Derived type is `cloudify.nodes.terraform.Module`

## Labels

The created deployment will have label `obj-type` equal to `service`