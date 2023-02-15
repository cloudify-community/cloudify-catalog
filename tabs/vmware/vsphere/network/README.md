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

| Name               | Type    | Description                                               | Default               |
| ------------------ | ------- | --------------------------------------------------------- | --------------------- |
| template_name      | string  | VM template name available in datastore                   | CentOS-7.8.2003-tmpl  |
| cpus               | string  | Number of virutal CPUs allocated to the VM                | 1                     |
| memory             | string  | Number of megabytes allocated to the VM                   | 1024                  |
| domain             | string  | VM network domain                                         | localdom              |
| dns_servers        | list    | List of DNS server to configure VM with                   | ['8.8.8.8']           |
| network_namei      | string  | Existing network to connect the VM to                     | Internal              |
| switch_distributed | boolean | specifies if connected network switch distributed         | false                 |
| use_dhcp           | boolean | specifies if VM should get IP from DHCP (if present)      | false                 |
| network_cidr       | string  | Connected network address in CIDR format                  | 172.16.168.0/24       |
| gateway_ip         | string  | Connected network gateway IP                              | 172.16.168.1          |
| vm_ip              | string  |  IP address assigned to the VM, if the DHCP is not in use | 172.16.168.201        |

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
