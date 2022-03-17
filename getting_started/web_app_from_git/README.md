# Application From Git Creation Example

## General

The blueprint is an example how to use cloudify WebServer and cloudify Application Module nodes for provisioning the example Calculator application. 

## Requirements

N/A 

## Secrets

N/A

## Plugins

N/A

## Inputs

| Display Label                               | Name                | Type   | Default Value                         |
| ------------------------------------------- | ------------------- | ------ | ------------------------------------- |
| The HTTP web server port                    | webserver_port      | int    | 8080                                  |
| A url of a web based javascript application | app_git             | string | https://github.com/zxcodes/Calculator |

## Node Types

### Http Web Server
The node type responsible for creation the WebServer application module.\
Derived type is `cloudify.nodes.WebServer`

### Web App
The node type responsible for creation the application from the Git repository.\
Derived type is `cloudify.nodes.ApplicationModule`

## Labels

N/A