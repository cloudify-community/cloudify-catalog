# AWS Environment Provisioning

## General

The blueprint creates AWS environment object in the Cloudify Manager. 

## Requirements

In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credentials to the AWS should have permission to describe, update, delete and create resources in the cloud provider environment. 


## Secrets

The blueprint uses secrets to connect to cloud, you need to connfigure them prior running the blueprint.

| Name                  | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| aws_access_key_id     | AWS Access Key ID                                                                  |
| aws_aceess_secret_key | AWS Access Secret Key                                                              |


## Plugins

N/A

## Inputs

| Display Laebel      | Name            | Type   | Default Value |
| ------------------- | --------------- | ------ | ------------- |
| AWS Regionn Name    | aws_region_name | string | us-east-1     |


## Node Types

N/A

## Labels

The created deployment will have label `obj-type` equal to `environment`
