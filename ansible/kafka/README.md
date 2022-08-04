# Kafka Provisioning

## General

The blueprint creates Kafka service with the Ansible plugin in the AWS/Azure cloud provider environment.

## Requirements

In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credentials to the AWS/Azure should have permission to describe, update, delete and created Virtual Machine.

## Secrets

The blueprint uses secrets to connect to AWS, you need to connfigure them prior running the blueprint.

| Name                  | Description           |
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key ID     |
| aws_aceess_secret_key | AWS Access Secret Key |

or 

The blueprint uses secrets to connect to Azure, you need to connfigure them prior running the blueprint.

| Name                  | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| azure_tenant_id       | Azure tenant ID                                                                    |
| azure_subscription_id | Azure subcription ID                                                               |
| azure_client_id       | Azure client ID                                                                    |
| azure_client_secret   | Azure client secret                                                                |

## Plugins

  - plugin:cloudify-fabric-plugin
  - plugin:cloudify-ansible-plugin

## Inputs

| Display Label                                                                                      | Name                | Type   | Default Value       |
| --------------------------------------------------------------------------------------------------- | ------------------- | ------ | ------------------- |
| Name of infrastructure blueprint to deploy.                                                         | infra_name          | string | aws                 |
| URL of infra zip file.                                                                              | infra_archive       | string | https://github.com/cloudify-community/cloudify-catalog/raw/6.4.0-build/docker/vm/vm.zip         |
| Whether a getting started infrastructure blueprint has already been uploaded to the manager or not. | infra_exists        | string | false               |
| The blueprint name, the deployment name.                                                            | infra_deployment_id | string | 'infra-{infra_name} |


## Node Types

### Infrastructure
The node type is responisble to create a Virtual Machine.
The type is `cloudify.nodes.Component`. 

### Security Group Rules
The node type is responisble to setup security group rules for infrastructure.
The type is `cloudify.nodes.Component`. 

### Kafka
The node types is responsible to run the playbook on the Virtual Machine.
The type is `cloudify.nodes.ansible.Playbook`. 


## Labels

The created deployment will have label `obj-type` equal to `service`