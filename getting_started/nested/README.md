# Nested Example

## General

The nested blueprint example - describes how you can create a multi-tier or distributed service where each service will have an independent blueprint and lifecycle operation similar to the way micro-services works.
We will illustrate how we can create a dependency and relationship between those services , pass inputs/output parameters etc.


## Requirements

Multi-Tier-Example needs to be imported from Getting Started Tab imported to the Cloudify Manager.

## Secrets

N/A

## Plugins

N/A

## Inputs

N/A

## Node Types

### Parent Blueprint
The node type is responsible for creation the example parent blueprint.\
Derived type is `cloudify.nodes.ServiceComponent`

### First Child Blueprint

The node type is responsible for creation the example child blueprint #1.\
Derived type is `cloudify.nodes.ServiceComponent`

### Second Child Blupeprint
The node type is responsible for creation the example child blueprint #2.\
Derived type is `cloudify.nodes.ServiceComponent`

## Labels

N/A