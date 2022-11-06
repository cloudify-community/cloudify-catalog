# Multicloud VM Provisioning

## General
The blueprint provision the virtual machine with preinstalled docker on the choosed cloud provider. Supported cloud provider are AWS, Azure and GCP.

## Requirmennts
In order to run successfully the blueprint you'll to provide credentials to the choosed cloud provider. 

## Secrets

In order to deploy to AWS, you need to configure secrets prior running the blueprint.

| Name                  | Description           |
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key ID     |
| aws_aceess_secret_key | AWS Access Secret Key |

In order to deploy to Azure, you need to configure secrets prior running the blueprint.

| Name                  | Description            |
| --------------------- | ---------------------- |
| azure_tenant_id       | Azure tenant ID        |
| azure_subscription_id | Azure subcription ID   |
| azure_client_id       | Azure client ID        |
| azure_client_secret   | Azure client secret    |

In order to deploy to GCP, you need to configure secrets prior running the blueprint.

| Name                  | Description                       |
| --------------------- | --------------------------------- |
| gcp_credentials       | GCP credentials json file content |


## Plugins

N/A 

## Inputs

| Display Label                           | Name                       | Type   | Description                                  | Default   |
| --------------------------------------- | -------------------------- | ------ | -------------------------------------------- | --------- |
| Provider name                           | provider_name              | string | Provider name such: AWS, Azure or GCP        | aws       |
| URL for secrets vallidation zip archive | secrets_validation_archive | string | URL for secrets vallidation zip archive      | N/A       |
| Secrets to validate                     | secrets_to_validate        | dict   | Provider secrets to check existence & values | N/A       |

## Node Types

### Secret Validation
The node type is responsible for validation of the existence & values of cloud credentials.\
Derived type is `cloudify.nodes.ServiceComponent`

### Virtual Machine
The node type is responsible for creation the virtual machine.\
Derived type is `cloudify.nodes.ServiceComponent`

## Labels
The created deployment will have label `obj-type` equal to `aws`

## Capabilities
Two properties are exposed:

| Name              | Description                                                        |
| ----------------- | ------------------------------------------------------------------ |
| endpoint          | The external endpoint of the application.                          |
| user              | User ID.                                                           |
| key_content       | Private agent key                                                  |
| security_group_id | Security group resource ID.                                        |
| vpc_id            | VPC resource ID.                                                   |
| vm_id             | VM resource ID.                                                    |
| rg_id             | Mock resource group id - to be compatible with Azure VM template   |