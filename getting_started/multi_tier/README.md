# Multi Tier Applicaiton Creation Example

## General

The multi tier blueprint example shows how you can use the Cloudify TOSCA based DSL to model relationships between multiple node types. 
We will use a multi tier topology of a classic web application

## Requirements

N/A 

## Secrets

N/A

## Plugins

N/A

## Inputs

| Display Label                            | Name                | Type   | Default Value |
| ---------------------------------------- | ------------------- | ------ | ------------- |
| The HTTP web server 1 port.              | webserver_port_1    | int    | 8001          |
| The HTTP web server 1 port.              | webserver_port_2    | int    | 8002          |
| The HTTP web server 1 port.              | webserver_port_3    | int    | 8003          |

## Node Types

### Demo Http Web Server 1
The node type responsible for creation the Http server #1.\
 `cloudify.nodes.WebServer`

### Demo Http Web Server 2
The node type responsible for creation the Http server #2.\
 `cloudify.nodes.WebServer`

### Demo Http Web Server 3
The node type responsible for creation the Http server #3.\
 `cloudify.nodes.WebServer`

### DB
The node type responsible for creation the database server.\
`cloudify.nodes.Database`

### Demo Load Balancer
The node type responsible for creation the load balancer module.\
`cloudify.nodes.LoadBalancer`

## Labels

N/A