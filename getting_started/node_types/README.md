# SSH Certificates Creation

## General

Node types  - describing how to map the lifecycle of simple resource.
In this specific example we use an http daemon as the resource.
The webserver/start.sh and stop.sh will be called to instantiate and decommission the service
The web server will run on the <manager host>:8000

## Requirements

N/A

## Secrets

N/A

## Plugins

N/A

## Inputs

| Display Label                            | Name                | Type   | Default Value |
| ---------------------------------------- | ------------------- | ------ | ------------- |
| The HTTP web server port                 | webserver_port      | string | 8000          |

## Node Types

### HTTP Web Server
The node type responsible for creation of the Web Server .\
Derived type is `cloudify.nodes.WebServer`

## Labels

N/A