# EC2 Provisioning

## General
The blueprint provisions the EC2 instance without the network, it is assumed that VPC has already been created and the subnet id is fetched from the input parameters.The blueprint generates public and private SSH keys. A Keypair is created with the public SSH key and attached to the provisioned EC2 instance. The public and private SSH keys are generated during the blueprint installation. The keys are stored in the Cloudify Manager secret store. 
If the secrets already exists the new one won't be generated. It will allow us to reuse the same keys for each provisioned EC2 instance and not having each time a new set of SSH keys.

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

| Display Label   | Name            | Type   | Description                      | Default   |
| --------------- | --------------- | ------ | -------------------------------- | --------- |
| AWS Region Name | region_name     | string | Select AWS Region Name           | us-east-1 |
| Instance Type   | instance_type   | string | Select instance type             | t2.micro  |
| Image ID        | image_id        | dict   | The map of regions and image ids | N/A       |
| AWS credentials | aws_credentials | dict   | The credentials for AWS          | N/A       |
| SSH Key secret name | ssh_key_secret_name | string | SSH Key secret name | N/A |
| Subnet ID | subnet_id | string | AWS Resource ID of the Subnet | N/A |
| Security Group ID | security_group_id | string | AWS Resource ID of the Security Group | N/A |
| EC2 name | ec2_name | string | Name of the EC2 instance | N/A |


## Node Types

### NIC
The node type is responsible for creating virtual network interface. 
The type is `cloudify.nodes.aws.ec2.Interface`.

### IP
The node type is responsible for creating public ip address.
The type is `cloudify.nodes.aws.ec2.ElasticIP`

### VM SSH KEY
The node type is responisble for generating public and private SSH keys.
The type is `cloudify.keys.nodes.RSAKey`. 

### CLOUD INIT
The node type is responsible for VM user config set up.
The type is `cloudify.nodes.CloudInit.CloudConfig`

### VM
To provision an ec2 instance we are using the type `cloudify.nondes.aws.ec2.Instances`. The instance type is passed as an input and the image id is selected based on the selected region.

The following AMi image will be provisioned per selected region

| Region      | AMi                   |
| ------------ | --------------------- |
| ca-central-1 | ami-033e6106180a626d0 |
| us-east-1    | ami-03248a0341eadb1f1 |
| us-west-1    | ami-01dd5a8ef26e6341d |
| us-west-2    | ami-024b56adf74074ca6 |
| eu-west-1    | ami-0eee6eb870dc1cefa |

## Labels
The created deployment will have label `obj-type` equal to `aws`

## Capabilities
Two properties are exposed:

| Name        | Description                                                |
| ----------- | ---------------------------------------------------------- |
| public_ip   | the public ip of the provisioned EC2 instance              |
| priavte_key | the private key that can be used to SSH to the `public_ip` |