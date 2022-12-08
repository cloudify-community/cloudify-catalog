terraform {
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "~>2.95.0"
    }
  }
}
# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}

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

variable "admin_login" {
  type = string
  default = "cloudify"
}

variable "subnet_a" {
  type = string
}

variable "subnet_b" {
  type = string
}

resource "random_password" "admin_password" {
  length = 12
  special = false
  min_lower = 1
  min_upper = 1
  min_numeric = 1
}

resource "azurerm_sql_server" "primary" {
  name                         = "${var.resource_prefix}primary"
  resource_group_name          = var.resource_group_a
  location                     = var.location_a
  version                      = "12.0"
  administrator_login          = var.admin_login
  administrator_login_password = random_password.admin_password.result
}

resource "azurerm_sql_server" "secondary" {
  name                         = "${var.resource_prefix}secondary"
  resource_group_name          = var.resource_group_b
  location                     = var.location_b
  version                      = "12.0"
  administrator_login          = var.admin_login
  administrator_login_password = random_password.admin_password.result
}

resource "azurerm_sql_database" "db" {
  name                = "${var.resource_prefix}cloudifydb"
  resource_group_name = azurerm_sql_server.primary.resource_group_name
  location            = azurerm_sql_server.primary.location
  server_name         = azurerm_sql_server.primary.name
}

resource "azurerm_sql_failover_group" "failover" {
  name                = "${var.resource_prefix}cloudify-db-dr"
  resource_group_name = azurerm_sql_server.primary.resource_group_name
  server_name         = azurerm_sql_server.primary.name
  databases           = [azurerm_sql_database.db.id]
  partner_servers {
    id = azurerm_sql_server.secondary.id
  }

  read_write_endpoint_failover_policy {
    mode          = "Automatic"
    grace_minutes = 60
  }
}

resource "azurerm_sql_firewall_rule" "primary-fw-rule" {
  name                = "primary-sql-fw-rule"
  resource_group_name = var.resource_group_a
  server_name         = azurerm_sql_server.primary.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}


resource "azurerm_sql_firewall_rule" "secondary-fw-rule" {
  name                = "secondary-sql-fw-rule"
  resource_group_name = var.resource_group_b
  server_name         = azurerm_sql_server.secondary.name
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "255.255.255.255"
}

resource "azurerm_sql_virtual_network_rule" "primary" {
  name                = "sql-vnet-rule"
  resource_group_name = var.resource_group_a
  server_name         = azurerm_sql_server.primary.name
  subnet_id           = var.subnet_a
}

resource "azurerm_sql_virtual_network_rule" "secondary" {
  name                = "sql-vnet-rule"
  resource_group_name = var.resource_group_b
  server_name         = azurerm_sql_server.secondary.name
  subnet_id           = var.subnet_b
}