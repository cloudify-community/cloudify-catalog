# Azure Storage Provisioning

## General
This blueprint creates an Azure storage account and resource group, and exposes the resulting account name as a capability

## Requirements
This blueprint you'll need Microsoft Azure API credentials, including a subscription ID, a tenant ID, a client ID, and a client secret.  The credentials must be sufficient to create resource groups and storage accounts

## Installaltion
Either pass Azure credential information in blueprint inputs (not recommended), or create the required secrets:

cfy secrets create -s XXXXX azure_subscription_id
cfy secrets create -s XXXXX azure_tenant_id
cfy secrets create -s XXXXX azure_client_id
cfy secrets create -s XXXXX azure_secret_key

```
## Required Plugins
* [Cloudify Azure Plugin](https://docs.cloudify.co/latest/working_with/official_plugins/infrastructure/azure/) - Used for Azure operation

## Inputs

| Name | Type | Description | Default |
| _______________ | _____________ | ______ | ______________________ | _________ |
| resource_prefix | string | prepend to created resources | '' |
| subscription_id | string | Azure subscrption ID | secret: azure_subscription_id|
| tenant_id | string | Azure tenant ID | secret: azure_tenant_id |
| client_id | string | Azure client ID | secret: azure_client_id |
| client_secret | string | Azure client secret | secret: azure_client_secret |
| account_type | string | Azure storage account type name | StandardLRS |
| location | string | Azure location name | EastUS |

## Blueprint Structure

The blueprint creates a resource group and a contained storage account.  The account resulting account name is exposed as a capability

## Capabilities

- `name` - the storage account name

