# Webserver Creation with Certificate Example

## General

The blueprint is an example how to use cloudify web server blueprint in the combination with certificate creation blueprint. 

## Requirements

The blueprint requires preuploaded getting started blueprints: 
* Certificate creation with the blueprint id equal to 'ex4GenSShCert' 
* Simple web server creation with the blueprint id equal to 'ex2SimpleWebServer' 

## Secrets

N/A

## Plugins

N/A

## Inputs

N/A

## Node Types

### Web Service Component
The node type responsible for creation the WebServer application.\
Derived type is `cloudify.nodes.ServiceComponent`

### WCertificate
The node type responsible for creation of the ssh certificate.\
Derived type is `cloudify.nodes.ServiceComponent`

## Labels

N/A