terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "2.95.0"
    }
  }
}

variable "resource_group_a" {
  type = string
}

variable "resource_group_b" {
  type = string
}

variable "location_a" {
  type = string
}

variable "location_b" {
  type = string
}

variable "resource_prefix" {
  type = string
  default = "xyz"
}

provider "azurerm" {
  features {}
}

resource "azurerm_storage_account" "storage_a" {
  name                     = "${var.resource_prefix}storagea"
  resource_group_name      = var.resource_group_a
  location                 = var.location_a
  account_tier             = "Standard"
  account_replication_type = "LRS"
  blob_properties {
    versioning_enabled  = true
    change_feed_enabled = true
  }
}

resource "azurerm_storage_container" "container_a" {
  name                  = "${var.resource_prefix}containerb"
  storage_account_name  = azurerm_storage_account.storage_a.name
  container_access_type = "private"
}

resource "azurerm_storage_account" "storage_b" {
  name                     = "${var.resource_prefix}storageb"
  resource_group_name      = var.resource_group_b
  location                 = var.location_b
  account_tier             = "Standard"
  account_replication_type = "LRS"
  blob_properties {
    versioning_enabled  = true
    change_feed_enabled = true
  }
}

resource "azurerm_storage_container" "container_b" {
  name                  = "${var.resource_prefix}containerb"
  storage_account_name  = azurerm_storage_account.storage_b.name
  container_access_type = "private"
}

resource "azurerm_storage_object_replication" "replica_config" {
  source_storage_account_id      = azurerm_storage_account.storage_a.id
  destination_storage_account_id = azurerm_storage_account.storage_b.id
  rules {
    source_container_name      = azurerm_storage_container.container_a.name
    destination_container_name = azurerm_storage_container.container_b.name
  }
}

output "primary_id" {
  value = azurerm_storage_account.storage_a.id
  sensitive = false
}

output "failover_id" {
  value = azurerm_storage_account.storage_b.id
  sensitive = false
}