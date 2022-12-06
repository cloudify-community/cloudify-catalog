# AKS Disaster Recovery Service Provisioning

## General

The blueprint creates AKS service across region configuration. The blueprint deploys EKS service with database, storage and load balancer in failover conifguration across two drifferent regions. 

## Requirments

In order to run successfully the blueprint you'll need Azure tenant id, subscription id, azure client id and client secret value. The credentials to the Azure should have permission to describe, update, delete and create resources in the cloud provider environment. 

## Secrets

The blueprint uses below secret in json format in order to set up service in Azure cloud. 

| Name                  | Description                        |
| --------------------- | ---------------------------------- |
| datadog_api_key       | API key for the Datadog monitoring |
| azure_tenant_id       | Azure tenant ID                    |
| azure_subscription_id | Azure subcription ID               |
| azure_client_id       | Azure client ID                    |
| azure_client_secret   | Azure client secret                |

## Plugins

* cloudify-azure-plugin
* cloudify-utilities-plugin
* cloudify-kubernetes-plugin
* cloudify-helm-plugin
* cloudify-terraform-plugin

## Inputs

| Display Laebel                                    | Name                  | Type   | Default Value |
| ------------------------------------------------- | --------------------- | ------ | ------------- |
| Azure location A                                  | azure_location_name_a | string | EastUs        |
| Azure location B                                  | azure_location_name_b | string | CentralUS     |
| The resource prefix for resources naming          | resource_prefix       | string | ''            |

## Node Types

## Key
The node type is responsible to create a SSH key pair.\
The type is `cloudify.keys.nodes.RSAKey`.

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