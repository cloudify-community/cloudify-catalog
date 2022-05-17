# AWS EKS Example

## General 

The blueprint creates EKS service with one node that is accessible from the public network.

## Requirements

  * Cloudify Manager with Latest AWS and Kubernetes Plugins.

### Secrets

The blueprint uses secrets to connect to AWS, you need to connfigure them prior running the blueprint.

| Name                  | Description           |
| --------------------- | --------------------- |
| aws_access_key_id     | AWS Access Key ID     |
| aws_aceess_secret_key | AWS Access Secret Key |

## Plugins

* cloudify-aws-plugin
* cloudify-utilities-plugin
* cloudify-kubernetes-plugin

## Inputs

| Display Label           | Name                       | Type   | Default Value                      |
| ----------------------- | -------------------------- | -------| ---------------------------------- |                                          
| AWS account access key  | aws_access_key_id          | string | { get_secret: awsc_access_key_id } |
| AWS account secret key  | aws_secret_access_key      | string | { get_secret: awsc_secret_key_id } |
| AWS region name         | aws_region_name            | string | us-east-1"                         |
| Availability Zone 1     | availability_zone_1_suffix | string | a                                  |
| Availability Zone 2     | availability_zone_2_suffix | string | b                                  |
| EKS Cluster name        | eks_cluster_name           | string | "k8s-cloudify"                     |
| EKS node group name     | eks_nodegroup_name         | string | eks_node_group_k8s-cloudify"       |
| Kubernetes version      | kubernetes_version         | string | ""                                 |
| Namespace to create     | service_account_namespace  | string | "deafult"                          |
| Service account name    | service_account_name       | string | "examples-user"                    |
| SSH key name            | ssh_keypair                | string | "eks_keyk8s-cloudify"              |
| Agent key name          | agent_key_name             | string | "agent_key"                        |

## Node Types

### Keypair 
The node type is responsible for generating ssh key pair.\
The type is `cloudify.nodes.aws.ec2.Keypair`.

### EKS service IAM Role
The node type is responsible for setting up service permissions.\
The type is `cloudify.nodes.aws.iam.Role`.

### EKS Nodegroup IAM Role
The node type is responsible for setting up node group permissions.\
The type is `cloudify.nodes.aws.iam.Role`.

### VPC 
The node type is responsible for creating the network for EKS deployment.\
The type is `cloudify.nodes.aws.ec2.Vpc`.

### Internet gateway
The node type is responsible for creating the Internet Gateway for EKS deployment.\
The type is `cloudify.nodes.InternetGateway`.

### Private/Public Subnets
The node type is responsible for creating the public & private subnets.\
The type is `cloudify.nodes.Subnet`.

### Private Route Tables
The node type is responsible for creating the route tables for deployment access.\
The type is `cloudify.nodes.RouteTable`.

### Public Route Internet Gateway
The node type is responsible for creating the Internet Gateway.\
The type is `cloudify.nodes.Route`.

### Elastic IPs
The node type is responsible for creating the public & private IPs.\
The type is `cloudify.nodes.ElasticIP`.

### NAT Gateway
The node type is responsible for creating the NAT gateway.\
The type is `cloudify.nodes.NATGateway`.

### Route Private Subnet Nat Gateways
The node type is responsible for creating the NAT gateway for private subnets.\
The type is `cloudify.nodes.Route`.

### Security group 
The node type is responsible for creating the security group for EKS deployment.\
The type is `cloudify.nodes.SecurityGroup`.

### Security group rules
The node type is responsible for creating the security rule for security group.\
The type is `cloudify.nodes.SecurityGroupRuleIngress`.

### EKS Cluster
The node type is responsible for creating EKS cluster service.\
The type is `cloudify.nodes.aws.eks.Cluster`.

### EKS Node Group 
The node type is responsible for adding the cluster to the specific node group.\
The type is `cloudify.nodes.aws.eks.NodeGroup`

### Kubernetes Master 
The node type is responsible for setting up the cluster configuration.\
The type is `cloudify.kubernetes.nodes.Master`

### New Service Account 
The node is responible for creating the new service account.\
The type is `cloudify.kubernetes.resources.ServiceAccount`.

### New Role Bindings 
The node is responsible for resource role binding for created service account.\
The type is `cloudify.kubernetes.resources.RoleBinding`.

### Secret
The node type is responsible for creating the secrets in K8s secret store.\
The type is `cloudify.kubernetes.resources.CustomBlueprintDefinedResource`.

### Store Token and Kubeconfig
The node type is responsible for creating the secret in manager resources.\
The type is `cloudify.nodes.Root`.

### Sanity Pod
The node type is responsible for deployment sanity pod in the K8s.\
The type is `cloudify.kubernetes.resources.FileDefinedResource`.

### Agent Key '
The node type is responsible for setting agent key.\
The type is `cloudify.keys.nodes.RSAKey`.

## Labels

The created deployment will have label `obj-type` equal to `k8s`



