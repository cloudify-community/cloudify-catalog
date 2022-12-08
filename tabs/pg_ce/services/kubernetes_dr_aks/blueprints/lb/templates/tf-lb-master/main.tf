terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "=2.95.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
}

variable "resource_group_name" {
    type = string
}

variable "fqdn_secondary" {
    type = string 
}

variable "fqdn_primary" {
    type = string
}

variable "resource_prefix" {
    type = string
}

resource "azurerm_traffic_manager_profile" "tm" {
  name                = "${var.resource_prefix}trafficmgr"
  resource_group_name = var.resource_group_name

  traffic_routing_method = "Weighted"

  dns_config {
    relative_name = "${var.resource_prefix}trafficmgr"
    ttl           = 100
  }

  monitor_config {
    protocol                     = "http"
    port                         = 80
    path                         = "/"
    interval_in_seconds          = 30
    timeout_in_seconds           = 9
    tolerated_number_of_failures = 3
  }
}

resource "azurerm_traffic_manager_endpoint" "primary" {
  name                = "trafficmgr_primary"
  resource_group_name = var.resource_group_name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  target              = var.fqdn_primary
  type                = "externalEndpoints"
  weight              = 50
}

resource "azurerm_traffic_manager_endpoint" "secondary" {
  name                = "trafficmgr_secondary"
  resource_group_name = var.resource_group_name
  profile_name        = azurerm_traffic_manager_profile.tm.name
  target              = var.fqdn_secondary
  type                = "externalEndpoints"
  weight              = 50
}

output "tm_endpoint" {
    value = azurerm_traffic_manager_profile.tm.fqdn
    sensitive = false
}