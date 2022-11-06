# Cost Estimation Service Provisioning

## General

The blueprint won't provision the services [EKS,RDS,S3] unless you run terraform `reload workflow` command.
but it gives you the terraform plan and cost of the modules 

## Requirements

In order to run successfully the blueprint you'll need AWS access key id and AWS access secret key. The credentials to the AWS should have permission to describe, update, delete and create deployment with cost estimation. Moreover you will need to provide `infracost_api_key` in order to get costs estimates - [details](https://www.infracost.io/docs/).

## Secrets

The blueprint uses secrets to connect to cloud, you need to connfigure them prior running the blueprint.


| Name                  | Description           |                                                                    
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key Id     |
| aws_aceess_secret_key | AWS Access Secret Key |
| infracost_api_key    | InfraCosts API Key    |

## Plugins

cloudify-terraform-plugin

## Inputs

| Display Label                            | Name                | Type   | Default Value  |
| ---------------------------------------- | ------------------- | ------ | -------------- |
| The password for database user           | password            | string | 'password'     |
| The resource prefix for resources naming | resource_prefix     | string | ''             |
| AWS region name                          | region_name         | string | 'us-west-1'    |

If the user provides empty value of default the prefix will be gerenated automatically.


## Node Types

### Secret Validation
The node type is responsible for validation of the existence & values of cloud credentials.\
Derived type is `cloudify.nodes.ServiceComponent`

### Infracosts
The node type responsible for deploying the terraform code.\
Derived type is `cloudify.nodes.ServiceComponent`


## Labels

The created deployment will have label `obj-type` equal to `service`