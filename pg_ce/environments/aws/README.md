# AWS Environment Provisioning

## General

The blueprint creates AWS Disaster Recovery environment object in the Cloudify Manager. 

## Requirements

In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credentials to the AWS should have permission to describe, update, delete and create resources in the cloud provider environment. 


## Secrets

The blueprint uses secrets to connect to cloud, you need to connfigure them prior running the blueprint.

| Name                  | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| aws_access_key_id     | AWS Access Key ID                                                                  |
| aws_aceess_secret_key | AWS Access Secret Key                                                              |
| aws_keypair           | AWS Keypair Name                                                                   |
| public_key_content    | The SSH public key (the actual contents) for the keypair specified by aws_keypair  |
| private_key_content   | The SSH private key (the actual contents) for the keypair specified by aws_keypair |


## Plugins

N/A

## Inputs

| Display Laebel       | Name              | Type     | Default Value |
| -------------------- | ----------------- | -------- | ------------- |
| AWS Region Name A    | aws_region_name_a | string   | us-east-1     |
| AWS Region Name B    | aws_region_name_b | string   | eu-west-1     |


## Node Types

N/A

## Labels

The created deployment will have label `obj-type` equal to `environment`