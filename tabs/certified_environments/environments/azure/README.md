# Azure Environment Provisioning

## General

The blueprint creates Azure environment object in the Cloudify Manager. 

## Requirements

In order to run successfully the blueprint you'll need Azure tenant id, subscription id, azure client id and client secret value. The credentials to the Azure should have permission to describe, update, delete and create resources in the cloud provider environment. 


## Secrets

The blueprint uses secrets to connect to cloud, you need to connfigure them prior running the blueprint.


| Name                  | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| azure_tenant_id       | Azure tenant ID                                                                    |
| azure_subscription_id | Azure subcription ID                                                               |
| azure_client_id       | Azure client ID                                                                    |
| azure_client_secret   | Azure client secret                                                                |


## Plugins

N/A

## Inputs

| Display Laebel   | Name                | Type   | Default Value |
| ---------------- | ------------------- | ------ | ------------- |
| Azure location   | azure_location_name | string | EastUs        |


## Node Types

N/A

## Labels

The created deployment will have label `obj-type` equal to `environment`
