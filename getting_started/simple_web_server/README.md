# Webserver Creation Example

## General

The blueprint is an example how to use cloudify WebServer node.

## Requirements

N/A 

## Secrets

N/A

## Plugins

N/A

## Inputs

| Display Label                            | Name                | Type   | Default Value |
| ---------------------------------------- | ------------------- | ------ | ------------- |
| The HTTP web server port                      | webserver_port               | int |8080        |

## Node Types

### My Resource
The node type responsible for creation the WebServer application module.\
Derived type is `cloudify.nodes.WebServer`

## Labels

N/A