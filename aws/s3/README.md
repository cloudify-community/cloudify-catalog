# S3 Bucket Provisioning

## General
The Blueprints provisions S3 Bucket and configures policy and lifecycle.

## Requirmennts
In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credenntials to the AWS should have permission to describe, update, delete and create S3 Bucket.

## Secrets

The blueprint uses secrets to connect to AWS, you need to connfigure them prior running the blueprint.

| Name                  | Description           |
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key ID     |
| aws_aceess_secret_key | AWS Access Secret Key |

## Plugins
cloudify-aws-plugin

## Inputs

| Display Lable   | Name            | Type   | Description              | Default       |
| ----------------| --------------- | ------ | ------------------------ | ------------- |
| AWS Region Name | aws_region_name | string | Select AWS Region Name   | us-east-1     |
| Queue Name      | queue_name      | string | The name of the queue    | test-queue    |



## Node Types

### SQS Queue
Creates an SQS Queue with the name provided by `queue_name` input.
The queue configured with 86400 MessageRetentionPeriod and 180 VisibilityTimeout

## Labels
The created deployment will have label `obj-type` equal to `aws`
