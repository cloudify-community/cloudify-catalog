# EBS Provisioning

## General

The blueprint creates EBS Volume of size 6gb in a provided availability zone

## Requirmennts

In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credenntials to the AWS should have permission to describe, update, delete and created Keypair and EC2 instannce.

## Secrets

The blueprint uses secrets to connect to AWS, you need to connfigure them prior running the blueprint.

| Name                  | Description           |
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key ID     |
| aws_aceess_secret_key | AWS Access Secret Key |

## Plugins

cloudify-aws-plugin Link and descriptionn what node type it coveres in the blueprinnt

cloudify-utilities-plugin Link

## Inputs

| Display Lable            | Name                     | Type   | Description              | Default   |
| ------------------------ | ------------------------ | ------ | ------------------------ | --------- |
| AWS Region Name          | aws_region_name          | string | Select AWS Region Name   | us-east-1 |
| Availability zone suffix | availability_zone_suffix | string | Availability zone suffix | a         |


## Node Types

### EBS Volume
the node type is responisble to create a EBS Volume.
The type is `cloudify.nodes.aws.ec2.EBSVolume`. 

For more details on the type can be found in the link

## Labels

The created deployment will have label `obj-type` equal to `aws`