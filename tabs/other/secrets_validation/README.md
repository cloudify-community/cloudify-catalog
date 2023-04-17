# Secret Validation AWS/Azure/GCP

## General
The blueprint validates the existance and correctness of the secrets values for following cloud providers: AWS, Azure and GCP. 

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

| Display Label                           | Name                 | Type   | Description                                                                     | Default   |
| --------------------------------------- | -------------------- | ------ | ------------------------------------------------------------------------------- | --------- |
| Provider name                           | provider             | string | The provider name for which the secret validation availability will be provided | aws       |
| Secrets list                            | secrets              | list   | Provider secrets to check existence & values                                    | N/A       |

## Node Types

### Secret Validation
The node type is responsible for validation of the existence & values of cloud credentials.\
Derived type is `cloudify.nodes.ServiceComponent`
