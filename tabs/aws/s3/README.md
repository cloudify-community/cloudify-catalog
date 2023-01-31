# S3 Bucket Provisioning

## General
The blueprint provisions an S3 bucket and configures policy and lifecycle.

## Requirmennts
In order to successfully deploy the blueprint you'll need AWS an access key id and secret access key. The credentials should have permission to describe, update, delete and create S3 buckets.

## Secrets

The blueprint uses secrets to connect to AWS, you need to configure them prior to deployment.

| Name                  | Description           |
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key ID     |
| aws_secret_access_key | AWS Secret Access Key |

## Plugins
cloudify-aws-plugin

## Inputs

| Display Label   | Name            | Type   | Description             | Default              |
| ----------------| --------------- | ------ | ------------------------| -------------------- |
| AWS Region Name | aws_region_name | string | Select AWS Region Name  | us-east-1            |
| Bucket Name     | bucket_name     | string | The name of the bucket  | test-cloudify-bucket |

## Node Types

### S3 Bucket
Creates an S3 bucket with the name provided by `bucket_name` input.
The bucket is configured with read/write access.

## Labels
The created deployment will have label `obj-type` equal to `aws`
