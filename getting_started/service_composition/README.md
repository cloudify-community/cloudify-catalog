# Service Composition Example

## General

Service Composition blueprint example - describes how to create relationship between independent services
In this case we run the same web server and application from ex3 as an independent deployment and were adding an SSH certificate generator to that service. The example will also demonstrate how we can upload and instantiate all nested services on demand.


## Requirements

N/A

## Secrets

N/A

## Plugins

N/A

## Inputs

N/A

## Node Types

### WebServiceComponent
The node type is responsible for creation of the Web Service.\
Derived type is `cloudify.nodes.ServiceComponent`

### Certificate
The node type is responsible for creation of the SSH Certificate.\
Derived type is `cloudify.nodes.ServiceComponent`

## Labels

N/A