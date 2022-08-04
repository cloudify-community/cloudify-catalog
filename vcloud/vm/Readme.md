# vSphere VM Provisioning

## General
The blueprint deploys a VM of specific flavor and template inside the vSphere environment

## Requirmennts
In order to run successfully the blueprint you'll need vSphere vCenter credentials, endpoint information and Resource Pool configured in vCenter. There has to be a network exisitng in the vCenter that the VM will connecto to.

## Secrets

The blueprint uses secrets to connect to ivSphere vCenter, you need to connfigure them prior running the blueprint.

| Name                       | Description                           |
| -------------------------- | ------------------------------------- |
| vcloud_user                | vCloud user name                      |
| vcloud_password            | vCloud password                       |
| vcloud_org                 | vCloud Org                            |
| vcloud_uri                 | vCloud URI                            |
| vcloud_vdc                 | vCloud VDC                            |
| vcloud_gateway             | vCloud Gateway                        |


## Plugins

cloudify-vsphere-plugin

## Inputs

| Name               | Type    | Description                                               | Default               |
| ------------------ | ------- | --------------------------------------------------------- | --------------------- |
| catalog            | string  | VM template name available in datastore                   | CentOS-7.8.2003-tmpl  |
| template           | string  | Number of virutal CPUs allocated to the VM                | 1                     |
| agent_key_name     | string  | Number of megabytes allocated to the VM                   | 1024                  |
| agen_user          | string  | VM network domain                                         | localdom              |


