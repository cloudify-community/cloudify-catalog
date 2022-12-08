# EC2 Provisioning

## General
The blueprint provisions the VPC with internet gateway, subnet, routetable and security group. 


## Requirmennts
In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credenntials to the AWS should have permission to describe, update, delete vpc, internet gateway, subnet, route table and security group. 

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

| Display Label   | Name            | Type   | Description                      | Default   |
| --------------- | --------------- | ------ | -------------------------------- | --------- |
| AWS Region Name | region_name     | string | Select AWS Region Name           | us-east-1 |
| AWS credentials | aws_credentials | dict   | The credentials for AWS          | N/A       |

## Node Types

### VPC
The node type is responsible for creating virtual network. 
The type is `cloudify.nodes.aws.ec2.Vpc`.

### Internet Gateway
The node type is responsible for creating internet gateway. 
The type is `cloudify.nodes.aws.ec2.InternetGateway`.

### Subnet
The node type is responsible for creating subnet. 
The type is `cloudify.nodes.aws.ec2.Subnet`.

### Route table
The node type is responsible for creating route table. 
The type is `cloudify.nodes.aws.ec2.RouteTable`.

### Route public subnet internet gateway
The node type is responsible for creating public subnet internet gateway. 
The type is `cloudify.nodes.aws.ec2.Route`.

### Security group 
The node type is responsible for creating security group. 
The type is `cloudify.nodes.aws.ec2.SecurityGroup` .

### Security group rules
The node type is responsible for creating secrity group rules. 
The type is `cloudify.nodes.aws.ec2.SecurityGroupRuleIngress`.

## Labels
The created deployment will have label `obj-type` equal to `aws`

## Capabilities
Two properties are exposed:

| Name              | Description                              |
| ----------------- | ---------------------------------------- |
| subnet_id         | AWS resource ID of the Subnet            |
| security_group_id | AWS resource ID of the Security Group    |
| vpc_id            | AWS resource ID of the VPC               |