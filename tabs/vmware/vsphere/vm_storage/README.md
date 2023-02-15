# vSphere VM with Storage Provisioning

## General
The blueprint deploys a VM of specific flavor and template inside the vSphere environment with defined size of the disk storage.

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
| vsphere_private_key        | Your SSH key to connect to VM         |

## Plugins

cloudify-vsphere-plugin
cloudify-fabric-plugin

## Inputs

| Name               | Type    | Description                                                  | Default               |
| ------------------ | ------- | ------------------------------------------------------------ | --------------------- |
| template_name      | string  | VM template available in datastore for ESXi hosts            | CentOS-7.9.2009-tmpl  |
| cpus               | string  | Number of virutal CPUs allocated to the VM                   | 1                     |
| memory             | string  | Number of RAM megabytes allocated to the VM                  | 1024                  |
| domain             | string  | Networking VM domain                                         | localdom              |
| dns_servers        | list    | Networking DNS servers provided to the configuration         | ['8.8.8.8']           |
| network_name       | string  | Network to connect VM to                                     | Internal              |
| switch_distributed | boolean | Is connected network switch distributed                      | false                 |
| use_dhcp           | boolean | Specifies if the connected network interface should use DHCP | false                 |
| network_cidr       | string  | Connected network address in CIDR format                     | 172.16.168.0/24       |
| gateway_ip         | string  | Connected network gateway IP                                 | 172.16.168.1          |
| vm_ip              | string  |  IP address assigned to the VM, if the DHCP is not in use    | 172.16.168.201        |

## Node Types

### VM
The node type is responisble for manageing the lifecycle of the vSphere hosted VM.
The type is `cloudify.vsphere.nodes.Server`.

### Storage
The node type is responsible for attaching the provisioned VM.
The type is `cloudify.vsphere.nodes.Storage`.

## Capabilities
Two properties are exposed:

| Name        | Description                                                |
| ----------- | ---------------------------------------------------------- |
| vm_ip       | the ip of the provisioned VM                               |
| vm_name     | the name of the provisioned VM                             |
