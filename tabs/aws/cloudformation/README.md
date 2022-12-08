# CloudFormation Provisioning

## General

The blueprint runs CloudFormation template from the directory to provision EC2.

## Requirmennts

In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credentials to the AWS should have permission to describe, update, delete and created DynamoDB Table.

## Secrets

The blueprint uses secrets to connect to AWS, you need to connfigure them prior running the blueprint.

| Name                  | Description           |
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key ID     |
| aws_aceess_secret_key | AWS Access Secret Key |


## Plugins

cloudify-aws-plugin
cloudify-utilities-plugin

## Inputs

| Display Laebel      | Name            | Type   | Default Value |
| ------------------- | --------------- | ------ | ------------- |
| AWS Regionn Name    | aws_region_name | string | us-east-1     |
| DynamoDB Table Name | dynamo_db_name  | string | MyApp         |

