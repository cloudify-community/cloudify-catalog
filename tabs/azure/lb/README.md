# Linux Provisioning

## General
This blueprint creates a Linux instance on Microsoft Azure, along with necessary networking services and a public IP.  The blueprint generates public and private SSH keys. A keypair (for SSH) is created, stored in the secret store, and attached to the provisioned instance.  If a secret with the same name(s) is present in the secret store, it is used.

## Requirements
This blueprint you'll need Microsoft Azure API credentials, including a subscription ID, a tenant ID, a client ID, and a client secret.  The credentials must be sufficient to create virtual machines and network elements such as networks, subnets, and public IP addresses.

## Installaltion
Either pass Azure credential information in blueprint inputs (not recommended), or create the required secrets:

cfy secrets create -s XXXXX azure_subscription_id
cfy secrets create -s XXXXX azure_tenant_id
cfy secrets create -s XXXXX azure_client_id
cfy secrets create -s XXXXX azure_secret_key

Additional optional secrets will be used for inputs `admin_username` and `admin_password`.  To use secrets, create the following:

cfy secrets create -s XXXXX azure_admin_usernae
cfy secrets create -s XXXXX azure_admin_password

```
## Required Plugins
* [Cloudify Azure Plugin](https://docs.cloudify.co/latest/working_with/official_plugins/infrastructure/azure/) - Used for Azure operation
* [Cloudify Utilities Plugin](https://docs.cloudify.co/latest/working_with/official_plugins/utilities/) - Used for keypair creation

## Inputs

| Name | Type | Description | Default |
| _______________ | _____________ | ______ | ______________________ | _________ |
| resource_prefix | string | prepend to created resources | '' |
| subscription_id | string | Azure subscrption ID | secret: azure_subscription_id|
| tenant_id | string | Azure tenant ID | secret: azure_tenant_id |
| client_id | string | Azure client ID | secret: azure_client_id |
| client_secret | string | Azure client secret | secret: azure_client_secret |
| vm_size | string | Azure location specific vm size name | Standard_B1S |
| location | string | Azure location name | EastUS |
| inage_publisher | string | Image publisher name | Canonical |
| image_offer | string | OS "offer"/product | UbuntuServer |
| image_sku | string | OS image SKU | 18.04-LTS |
| image_version | string | OS image version | latest |
| admin_username | string | server admin user name | secret: azure_admin_username |
| admin_password | string | server admin password | secret: azure_admin_password |

## Blueprint Structure

The blueprint creates a resource group that all other elements refer to.  It creates a  public IP, a virtual network, a subnet, an IP configuration to select DHCP, a security group to allow SSH, a network interface (NIC), a storage account, and finally a virtual machine configured from the blueprint inputs.

## Capabilities

Two capabilities are exposed:
- `public_ip` - the public ip of the provisioned instance
- `private_key` - the private key that can be used to SSH to the instance

