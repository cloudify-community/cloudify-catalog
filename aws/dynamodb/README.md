# DynamoDB Table Provisioning

## General

The blueprint creates DynamoDB with a RandomKeyUUID key name and ReadCapacity and WriteCapacity set to 5.

## Requirmennts

In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credenntials to the AWS should have permission to describe, update, delete and created Keypair and EC2 instannce.

## Secrets

The blueprint uses secrets to connect to AWS, you need to connfigure them prior running the blueprint.

aws_access_key_id - AWS Access Key ID
aws_aceess_secret_key - AWS Access Secret Key

## Inputs

| Display Laebel      | Name            | Type   | Default Value |
| ------------------- | --------------- | ------ | ------------- |
| AWS Regionn Name    | aws_region_name | string | us-east-1     |
| DynamoDB Table Name | dynamo_db_name  | string | MyApp         |

## Plugins

cloudify-aws-plugin Link and descriptionn what node type it coveres in the blueprinnt

cloudify-utilities-plugin Link

## Inputs

| Display Lable   | Name          | Type   | Description            | Default   |
| --------------- | ------------- | ------ | ---------------------- | --------- |
| AWS Region Name | region_name   | string | Select AWS Region Name | us-east-1 |
| Instance Type   | instance_type | string | Select instance type   | t2.micro  |

## Node Types

### DynamoDB Table
the node type is responisble to create a DynamoDB Table.
The type is `cloudify.nodes.aws.dynamodb.Table`. 

For more details on the type can be found in the link

## Labels

The created deployment will have label `obj-type` equal to `aws`