# EC2 Provisioning

## General
The blueprint provisions the EC2 instance and installs the Cloudify Manager from the predefined rpm url. 

## Requirmennts
In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credenntials to the AWS should have permission to describe, update, delete and created Keypair and EC2 instannce.

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

| Display Label                | Name            | Type   | Description                       | Default   |
| ---------------------------- | --------------- | ------ | --------------------------------- | --------- |
| URL for Cloudify Manager rpm | rpm_url         | string | Cloudify Manager installation RPM | N/A       |
| URL for vm zip archive       | vm_archive      | string | URL of vm zip file                | N/A       |
| URL for network zip archive  | netwrok_archive | string | URL of network zip file           | N/A       |
| AWS Region Name              | region_name     | string | Select AWS Region Name            | us-east-1 |



## Node Types

### Network
The node type is responsible for creating virtual network. 
The type is `cloudify.nodes.ServiceComponent`.

### Security group
The node type is responsible for referencing security group.
The type is `cloudify.nodes.aws.ec2.SecurityGroup`

### Security group rules
The node type is responisble for creating security group rules.
The type is `cloudify.nodes.aws.ec2.SecurityGroupRuleIngress`. 

### Cloudify manager VM
The node type is responsible for creating VM instance.
The type is `cloudify.nodes.ServiceComponent`

### Cloudify manager install
The node type installs and configure the Cloudify Manager.
The type is `cloudify.nodes.Root`


## Labels
The created deployment will have label `obj-type` equal to `aws`

## Capabilities
Two properties are exposed:

| Name                       | Description                                   |
| -------------------------- | --------------------------------------------- |
| cloudify_manager_endpoint  | the public ip of the provisioned EC2 instance |