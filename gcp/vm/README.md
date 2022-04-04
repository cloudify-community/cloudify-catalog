# VM Provisioning

## General

The blueprint creates Centos VM with the usage of the GCP Cloudify plugin.

## Requirements

Install sercrets and plugins listed below, no specific requriements needed. 

## Secrets

The blueprint uses below secrets in order to set up service in GCP cloud.

| Name                     | Description                                    |
| ------------------------ | -----------------------------------------------|
| gcp_client_x509_cert_url | certificate url from the GCP secret json file  |
| gcp_client_email         | client email from the GCP secret json file     |
| gcp_client_id            | client id from the GCP secret json file        |
| gcp_project_id           | project id from the GCP secret json file       |
| gcp_private_key_id       | private key id from the GCP secret json file   |
| gcp_private_key          | private key from the GCP secret json file      |                                  

## Plugins

cloudify-gcp-plugin
cloudify-utilities-plugin

## Inputs

| Display Label                                                             | Name             | Type   | Default Value                                                                                  |
| ------------------------------------------------------------------------- | ---------------- | ------ | ---------------------------------------------------------------------------------------------  |
| The GCP region to deploy the application in, such as europe-west1.        | region           | string | 'europe-west1'                                                                                 |
| The GCP zone to deploy the application in, such as europe-west1-b.        | zone             | string | 'europe-west1-b'                                                                               |
| URL to the Centos image.                                                  | image            | string | 'https://www.googleapis.com/compute/v1/projects/centos-cloud/global/images/centos-7-v20191210' |
| A small GCP machine type.                                                 | instance_type    | string | n1-standard-2                                                                                  |
| The username of the agent running on the instance created from the image. | agent_user       | string | 'centos'                                                                                       |
| Agent key name                                                            | agent_key_name   | string | agent_key                                                                                      |
| Control parameters for names in resources.                                | env_name         | string | 'example'                                                                                      |

## Node Types

### VM
The node is responsible for virtual machine deployment.\
The type is `cloudify.gcp.nodes.Instance`.

### Disk
The node is responsible for provisioning VM with the storage.\
The type is `cloudify.gcp.nodes.Volume`.

### Firewall
The node is responsible for setting up the firewall rules for the VM access.\
The type is `cloudify.gcp.nodes.FirewallRule`.

### Firewall
The node is responsible for setting up the firewall rules for the VM access.\
The type is `cloudify.gcp.nodes.FirewallRule`.

### Subnet
The node is responsible for setting up the network for the VM.\
The type is `cloudify.gcp.nodes.Network`.

### Network
The node is responsible for setting up the sub-network for the VM.\
The type is `cloudify.gcp.nodes.SubNetwork`.

### Agent Key
The node is responsible for generation of ssh keys for the VM.\
The type is `cloudify.gcp.nodes.RSAkey`.

## Labels

The created deployment will have label `obj-type` equal to `service` & `vm`