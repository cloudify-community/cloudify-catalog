# PostgreSQL Provisioning

## General

The blueprint creates PostgreSQL DB with a default postgres user and database. 

Supported Cloud Providers:

 * AWS
 * Azure

## Requirmennts

### AWS

In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credentials to the AWS should have permission to describe, update, delete and create VM and VPC.

### Azure

In order to run successfully the blueprint you'll need Azure subscription id, tenant id, client id and client secret value. The credentials to the Azure should have permission to describe, update, delete and create resource group, VM and virtual network.

## Secrets

The blueprint uses secrets to connect to cloud, you need to connfigure them prior running the blueprint.

### AWS

| Name                  | Description           |
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key ID     |
| aws_aceess_secret_key | AWS Access Secret Key |

### Azure

| Name                  | Description           |
| --------------------- | --------------------- |
| azure_tenant_id       | Azure tenant ID       |
| azure_subscription_id | Azure subscription ID |
| azure_client_id       | Azure client ID       |
| azure_client_secret   | Azure client secret   |



## Plugins

cloudify-aws-plugin

## Inputs

| Display Laebel      | Name            | Type   | Default Value |
| ------------------- | --------------- | ------ | ------------- |
| AWS Regionn Name    | aws_region_name | string | us-east-1     |
| DynamoDB Table Name | dynamo_db_name  | string | MyApp         |


## Node Types

### DynamoDB Table
the node type is responisble to create a DynamoDB Table.
The type is `cloudify.nodes.aws.dynamodb.Table`. 

For more details on the type can be found in the link

## Labels

The created deployment will have label `obj-type` equal to `aws`
