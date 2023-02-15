# vSphere VM Provisioning

## General
The blueprint deploys a VM of specific flavor and template inside the vSphere environment

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

| Name               | Type    | Description                      | Default          |
| ------------------ | ------- | -------------------------------- | ---------------- |
| switch_distributed | boolean | Network Interface configuration  | false            |
| network_name       | string  | Network name to create           | cloudify_network |
| vlan_id            | string  | Virtual network name to create   | false            |
| vswitch_name       | string  | Virtual switch name to create    | vSwitch0         |



## Node Types

### Nic
The node type is responisble for manageing the lifecycle of the vSphere network interface.
The type is `cloudify.vsphere.nodes.NIC`. 

### Net
The node type is responisble for manageing the lifecycle of the vSphere network.
The type is `cloudify.vsphere.nodes.Network`. 

## Capabilities
Two properties are exposed:

| Name        | Description                                            |
| ----------- | ------------------------------------------------------ |
| net_id      | ID of provisioned network                              |
