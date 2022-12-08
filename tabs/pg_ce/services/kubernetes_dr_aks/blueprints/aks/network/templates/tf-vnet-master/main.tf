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

variable "azure_location_name" {
    type = string
}

variable "resource_group_name" {
    type = string
}

variable "vnet_name" {
    type = string
}

variable "subnet_1_name"{
    type = string
}

variable "subnet_2_name" {
    type = string
}

variable "sa_name" {
    type = string
}

variable "pip1_name" {
    type = string
}

variable "pip2_name" {
    type = string
}

resource "azurerm_resource_group" "rg" {
  name = var.resource_group_name
  location = var.azure_location_name
}

resource "azurerm_virtual_network" "vnet" {
  name                = var.vnet_name
  location            = var.azure_location_name
  resource_group_name = azurerm_resource_group.rg.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "subnet_1" {
  name                 = var.subnet_1_name
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.0.0/23"]
  service_endpoints    = ["Microsoft.Sql"]
}

resource "azurerm_subnet" "subnet_2" {
  name                 = var.subnet_2_name
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/23"]
  service_endpoints    = ["Microsoft.Sql"]
}

resource "azurerm_storage_account" "sa" {
  name                     = var.sa_name
  location                 = var.azure_location_name
  resource_group_name      = azurerm_resource_group.rg.name
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_public_ip" "pip1" {
  name                = var.pip1_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  domain_name_label   = "${var.resource_group_name}1"
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_public_ip" "pip2" {
  name                = var.pip2_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  domain_name_label   = "${var.resource_group_name}2"
  allocation_method   = "Static"
  sku                 = "Standard"
}

data "azurerm_public_ip" "pip2" {
  name                =  azurerm_public_ip.pip2.name
  resource_group_name =  azurerm_resource_group.rg.name
}

data "azurerm_public_ip" "pip1" {
  name                = azurerm_public_ip.pip1.name
  resource_group_name = azurerm_resource_group.rg.name
}