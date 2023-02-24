# vSphere Pool Provisioning

## General
The blueprint deploys a Pool of specific flavor inside the vSphere environment.

## Requirements
In order to run successfully the blueprint you'll need vSphere vCenter credentials, endpoint information and Resource Pool configured in vCenter. There has to be a network exisitng in the vCenter that the VM will connecto to.

## Secrets

The blueprint uses secrets to connect to ivSphere vCenter, you need to connfigure them prior running the blueprint.

| Name                       | Description                           |
| -------------------------- | ------------------------------------- |
| vsphere_username           | vCenter user name                     |
| vsphere_password           | vCenter password                      |
| vsphere_host               | vCenter hosname / IP                  |
| vsphere_port               | vCenter TCP port                      |
| vsphere_resource_pool_name | Existing Resource Pool name           |
| vsphere_datacenter_name    | Datacenter name in vCenter            |
| vsphere_auto_placement     | VM autoplacement flag                 |
| vsphere_allow_insecure     | Allow insecure connections to vCenter |

## Plugins

cloudify-vsphere-plugin

## Inputs

| Name               | Type    | Description                    | Default               |
| ------------------ | ------- | -----------------------------  | --------------------- |
| pool_name          | string  | Pool name to create            | cloudify_test_pool    |
| cluster_name       | string  | Cluster name to deploy pool    | cloudify              |


## Node Types

### Pool
The node type is responisble for manageing the lifecycle of the vSphere pool.
The type is `cloudify.vsphere.nodes.ResourcePool`. 

## Capabilities
Two properties are exposed:

| Name        | Description                                                |
| ----------- | ---------------------------------------------------------- |
| vm_ip       | the ip of the provisioned VM                               |
| vm_name     | the name of the provisioned VM                             |