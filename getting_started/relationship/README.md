# Relationship Example

## General

The relationship blueprint describes how to create dependencies between multiple node types resources
In this case were adding a web application node (web calculator) that will be contained_in the http_web_server resource
Note that the application is pulled from a git repository and can be easily modified to any other application as needed.
See the app_scripts/create.sh to see how this is done.
The webserver and application will run on the <manager host>:8000

## Requirements

N/A

## Secrets

N/A

## Plugins

N/A

## Inputs

| Display Label                               | Name                | Type   | Default Value                         |
| ------------------------------------------- | ------------------- | ------ | ------------------------------------- |
| The HTTP web server port                    | webserver_port      | string | 8000                                  |
| A url of a web based javascript application | app_git             | string | https://github.com/zxcodes/Calculator |

## Node Types

### Web Service Component
The node type responsible for creation the WebServer application.\
Derived type is `cloudify.nodes.ServiceComponent`

### WCertificate
The node type responsible for creation of the ssh certificate.\
Derived type is `cloudify.nodes.ServiceComponent`

## Labels

N/A