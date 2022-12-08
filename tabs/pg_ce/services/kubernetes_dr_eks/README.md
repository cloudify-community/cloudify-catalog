# EKS Disaster Recovery Service Provisioning

## General

The blueprint creates EKS service across region configuration. The blueprint deploys EKS service with database, storage and load balancer in failover conifguration across two drifferent regions. 

## Requirmennts

In order to run successfully the blueprint you'll need AWS access key id and aceess secret key. The credentials to the AWS should have permission to describe, update, delete and create resources in the cloud provider environment. 

## Secrets

The blueprint uses below secret in json format in order to set up service in AWS cloud.

| Name                  | Description                        |
| --------------------- | ---------------------------------- |
| datadog_api_key       | API key for the Datadog monitoring |
| aws_access_key_id     | AWS Access Key ID                  |
| aws_access_secret_key | AWS Access Secret Key              |

## Plugins

* cloudify-aws-plugin
* cloudify-kubernetes-plugin
* cloudify-helm plugin
* cloudify-utilities-plugin

## Inputs

| Display Label                            | Name                | Type              | Default Value                                    |
| ---------------------------------------- | ------------------- | ----------------- | ------------------------------------------------ |
| The resource prefix for resources naming | resource_prefix     | string            | ''                                               |
| The domain for load balancer creation    | domain_owned        | string            | aws.com                                          |
| AWS Region Name A                        | aws_region_name_a   | string            | us-east-1                                        |
| AWS Region Name B                        | aws_region_name_b   | string            | eu-west-1                                        |

## Node Types

### Prefix
The node type is responsible to create a Prefix for the purpose of naming resources.\
The type is `eaas.nodes.UniquePrefixGenerator`.

For more details on the type can be found in the [link](https://github.com/cloudify-community/eaas-example/blob/master/utils/custom_types.yaml)

### AKS Cluster A
The node type is responsible for creating the primary cluster with the vpc for EKS DR deployment.\
The type is `cloudify.nodes.ServiceComponent`.

### AKS Cluster B
The node type is responsible for creating the failover cluster with the vpc for EKS DR deployment.\
The type is `cloudify.nodes.ServiceComponent`.

### S3 
The node type is reponsible for ceating the bucket storage for EKS DR deployment.\
The type is `cloudify.nodes.ServiceComponent`.

### Database
The node type is reponsible for creating the database for EKS DR deployment.\
The type is `cloudify.nodes.ServiceComponent`.

### Load Balancer
The nde type is reponsible for creating the application load balancer for EKS DR deployment.\
The type is `cloudify.nodes.ServiceComponent`.

## Labels

The created deployment will have label `obj-type` equal to `service`