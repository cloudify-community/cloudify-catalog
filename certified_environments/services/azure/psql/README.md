# PostgreSQL Service Provisioning

## General

The blueprint creates PostgreSQL database service with default postgres user the virtual machine accessible for the user by SSH protocol.

## Requirements

In order to run successfully the blueprint you'll need to provide the Azure environment - details [here](https://github.com/cloudify-community/eaas-example). 

## Secrets

The blueprint uses below secret in json format in order to set up service in Azure cloud - the example of the secret format could be found [here](https://github.com/cloudify-community/eaas-example/blob/master/secret.json).

| Name                  | Description                                            |
| --------------------- | ------------------------------------------------------ |
| eeas_params           | The virtual machine & network service configuration    |


## Plugins

cloudify-fabric-plugin

## Inputs

| Display Label                            | Name            | Type   | Default Value  |
| ---------------------------------------- | --------------- | ------ | -------------- |
| The resource prefix for resources naming | resource_prefix | string | ''             |

If the user provides empty value of default the prefix will be gerenated automatically.

## Node Types

### Prefix
the node type is responsible to create a Prefix for the purpose of naming resources.\
The type is `eaas.nodes.UniquePrefixGenerator`.

For more details on the type can be found in the [link](https://github.com/cloudify-community/eaas-example/blob/master/utils/custom_types.yaml)

### Network
the node type is responsible for creating the network & VM form minikube deployment.\
The type is `cloudify.nodes.ServiceComponent`.

### Database
the node type responsible for installation, configuration & start PostgreSQL server.\
Derived type is `cloudify.nodes.Root`

## Labels

The created deployment will have label `obj-type` equal to `service`