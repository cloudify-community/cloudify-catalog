# AKS Disaster Recovery Service Provisioning

## General

The blueprint creates AKS service across region configuration. The blueprint deploys EKS service with database, storage and load balancer in failover conifguration across two drifferent regions. 

## Requirmennts

In order to run successfully the blueprint you'll need to provide the Azure DR environment - details [here](https://github.com/cloudify-community/eaas-example). 

## Secrets

The blueprint uses below secret in json format in order to set up service in Azure cloud - the example of the secret format could be found [here](https://github.com/cloudify-community/eaas-example/blob/master/secret.json).

| Name                  | Description                        |
| --------------------- | ---------------------------------- |
| datadog_api_key       | API key for the Datadog monitoring |


## Plugins

* cloudify-azure-plugin
* cloudify-kubernetes-plugin
* cloudify-helm-plugin
* cloudify-terraform-plugin

## Inputs

| Display Label                                      | Name              | Type                  | Default Value                                    |
| -------------------------------------------------- | --------------------| ------------------- | ------------------------------------------------ |
| Cloud Credentials from Azure env. with location A  | cloud_credentials_a | cloud_credentials_a | Please look at the cloud_credentials type legend |
| Cloud Credentials from Azure env. with location B  | cloud_credentials_b | cloud_credentials_b | Please look at the cloud_credentials type legend |
| The resource prefix for resources naming           | resource_prefix     | string              | ''                                               |

### Custom types
cloud_credentials_a
| Property Name             | Type   | Default Value                         |
| ------------------------- | ------ | ------------------------------------- |
| azure_tentant_id          | string | gets from cloud Azure env. capability |
| azure_subscription_id     | string | gets from cloud Azure env. capability |
| azure_client_id           | string | gets from cloud Azure env. capability |
| azure_client_secret       | string | gets from cloud Azure env. capability |
| public_key_content        | string | gets from cloud Azure env. capability |
| private_key_content       | string | gets from cloud Azure env. capability |
| region_name_a             | string | gets from cloud Azure env. capability |

cloud_credentials_b
| Property Name             | Type   | Default Value                         |
| ------------------------- | ------ | ------------------------------------- |
| azure_tentant_id          | string | gets from cloud Azure env. capability |
| azure_subscription_id     | string | gets from cloud Azure env. capability |
| azure_client_id           | string | gets from cloud Azure env. capability |
| azure_client_secret       | string | gets from cloud Azure env. capability |
| public_key_content        | string | gets from cloud Azure env. capability |
| private_key_content       | string | gets from cloud Azure env. capability |
| region_name_b             | string | gets from cloud Azure env. capability |


resource_config
| Property Name             | Type   | Default Value |
| ------------------------- | ------ | ------------- |
| kubernetes_version        | string | ''            |
| service_account_namespace | string | default       |
| service_cidr              | string | 10.0.8.0/23   |
| docker_bridge             | string | 10.0.10.1/23  |
| dns_service_ip            | string | 10.0.8.2      |
| node_pool_size            | string | 1             |

## Node Types

### Prefix
The node type is responsible to create a Prefix for the purpose of naming resources.\
The type is `eaas.nodes.UniquePrefixGenerator`.

For more details on the type can be found in the [link](https://github.com/cloudify-community/eaas-example/blob/master/utils/custom_types.yaml)

### AKS Cluster A
The node type is responsible for creating the AKS primary cluster deployment with the network stack.\
The type is `cloudify.nodes.ServiceComponent`.

### AKS Cluster B
The node type is responsible for creating the AKS failover cluster deployment with the network stack.\
The type is `cloudify.nodes.ServiceComponent`.

### Load Balancer
The nde type is reponsible for creating the application load balancer for EKS DR deployment.\
The type is `cloudify.nodes.ServiceComponent`.

### Storage
The node type is reponsible for ceating the bucket storage for AKS DR deployment.\
The type is `cloudify.nodes.ServiceComponent`.

### Database
The node type is reponsible for creating the database for AKS DR deployment.\
The type is `cloudify.nodes.ServiceComponent`.


## Labels

The created deployment will have label `obj-type` equal to `service`