# SSH Certificates Creation

## General

The blueprint creates a pair of SSH keys and saves them in the cloudify manager as secrets.

## Requirements

In order to run successfully the blueprint you'll need to install required plugins and provide the manager with required inputs. 

## Secrets

N/A

## Plugins

cloudify-utilities-plugin

## Inputs

| Display Label                            | Name                | Type   | Default Value |
| ---------------------------------------- | ------------------- | ------ | ------------- |
| The prefix name for the keypair          | key_name            | string | MyKey         |

## Node Types

### SSH Key
The node type responsible for creation the SSH key pair.\
Derived type is `cloudify.keys.nodes.RSAKey`

## Labels

N/A