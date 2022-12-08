# EC2 Spot Instance Provisioning

## General
The Blueprints provisions provisioning a newtork layer, EC2 with EBS attached to it. The network layer contains of VPC, Subnet, Security Group, Internet Gateway and Routing.

As part of the provisioning SSH Key is generated and propogated to the EC2 instance. The SSH Key can be used to connect to the EC2 instance.

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

| Display Lable                | Name                         | Type   | Description              | Default       |
| ---------------------------- | ---------------------------- | ------ | ------------------------ | ------------- |
| AWS Region Name              | aws_region_name              | string | Select AWS Region Name   | us-east-1     |
| Availability Zone Suffix     | availability_zone_suffix     | string | Availability Zone        | a             |
| VPC CIDR                     | vpc_cidr                     | string | VPC CIDR                 | 10.10.0.0/16  |
| Public Subnet CIDR           | public_subnet_cidr           | string | Public subnet CIDR       | 10.10.0.0/24  |
| EBS Volume Attachment Device | ebs_volume_attachment_device | string | EC2 instance type        | t2.micro      |
| Key Name                     | key_name                     | string | Key name                 | test-key      |
| Instance Type                | instance_type                | string | EC2 Instance Tpe         | t2.medium     |
| Volume Attachment Device     | volume_attachment_device     | string | Volume Attachment Device | /dev/sdh      |



## Node Types

### EC2 Spot Instance
To provision an ec2 spot instance we are using the type `cloudify.nodes.aws.ec2.SpotInstances`. 
The instance type is passed as an input. The AMi id is selected based on the AMi Owner and AMi Name filters.

### AMi
Looks for AMi id based on the owner and name filter and passes it to EC2 Spot Instance.

### IP
Provisions an elastic IP which will be connected to the Netowrk Interface that will be assigned to EC2 Spot Instance.

### NIC
Network Interface withing a provisioned subnet for EC2 spot instance

### Security Group Riles
Defines what ports are opened and to what CIDRs

### Security Group
Creates a security group within the provisioned VPC

### Internet Gateway
Creates Internet Gateway for VPC

### Route
Creates a route between internet gateway and subnet within VPC

### Subnet Creates Subnet within the VPC

### Creates a VPC
Creates a VPC

### Cloud Init
Configures SSH Key for the provisioned EC2 spot instance.

## Labels
The created deployment will have label `obj-type` equal to `aws`
