# EKS Service Provisioning

## General

The blueprint creates EKS service with one node that is accessible from the public network.

## Requirmennts

In order to run successfully the blueprint you'll need to provide the AWS environment - details [Here](https://github.com/cloudify-community/eaas-example). 

## Secrets

The blueprint uses secrets to connect to AWS, you need to connfigure them prior running the blueprint.

| Name                  | Description           |
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key ID     |
| aws_aceess_secret_key | AWS Access Secret Key |


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

The created deployment will have label `obj-type` equal to `service`