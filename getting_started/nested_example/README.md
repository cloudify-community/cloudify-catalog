# Nested Application Creation Example

## General

The nested blueprint example illustrates how you can create a multi-tier or distributed service where each service will have an independent blueprint and lifecycle operation similar to thethey way micro-services works. We will illustrate how we can create a dependency and relationship between those services , pass inputs/output parameters etc.

To do that we are using a feature that is referred to as  Service Composition. The Service Composition node type allows us to wrap an external service and expose it as a local node type. This allows us to leverage the relationship and dependency management and the rest of the  blueprint feature just as you would with a regular blueprint.

In the following example we are using two blueprints.
ChildBP1, and ChildBP2 are node types that are pointing to a blueprint with different params. The two node types  act as two independent services and a parent blueprint that will use the service component feature to call the child services.


## Requirements

 In this specific example we use the same multi-tier blueprint across all the three service components and deploy it under a different deployment name( multi-tier-example, multi-tier-example-1, multi-tier-example-2).  In reality it is more likely that each component will point to a separate blueprint per component.

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