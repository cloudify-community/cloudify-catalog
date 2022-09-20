# EKS Service with Istio Provisioning

## General

The blueprint creates EKS service based on the terraform hashicorp [example](https://github.com/hashicorp/learn-terraform-provision-eks-cluster) then use Istio helm inside terraform as well.

## Requirements

In order to run successfully the blueprint you'll need AWS access key id and AWS secret access key. The credentials to the AWS should have permission to describe, update, delete and create EKS and VPC services.

The blueprint use git command so please ensure that git is installed in the Cloudify manager.

## Secrets

The blueprint uses secrets to connect to cloud, you need to configure them prior running the blueprint.


| Name                  | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| aws_access_key_id     | AWS Access Key ID                                                                  |
| aws_aceess_secret_key | AWS Access Secret Key                                                              |

## Plugins

cloudify-terraform-plugin

## Inputs

| Display Label                            | Name                | Type   | Default Value |
| ---------------------------------------- | ------------------- | ------ | ------------- |
| AWS region name                          | region              | string | us-east-1     |

If the user provides doesn't provide override values it will use default ones.


## Node Types

### Terraform
The node type is responsible for configuration the host for terraform.\
The type is `cloudify.nodes.terraform`.

### Terraform Module
The node type responsible for deploying the terraform code.\
Derived type is `cloudify.nodes.terraform.Module`

## Labels

The created deployment will have label `obj-type` equal to `environment`
