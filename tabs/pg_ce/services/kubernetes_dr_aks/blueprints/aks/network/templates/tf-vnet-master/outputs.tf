output "pip1_id" {
    value = data.azurerm_public_ip.pip1.id
    sensitive = false
}

output "pip1_fqdn" {
    value = data.azurerm_public_ip.pip1.fqdn
    sensitive = false
}

output "pip1" {
    value = data.azurerm_public_ip.pip1.ip_address
    sensitive = false
}

output "pip2_id" {
    value = data.azurerm_public_ip.pip2.id
    sensitive = false
}

output "pip2_fqdn" {
  value = data.azurerm_public_ip.pip2.fqdn
  sensitive = false
}

output "pip2" {
  value = data.azurerm_public_ip.pip2.ip_address
  sensitive = false
}

output "vn_id"{
    value = azurerm_virtual_network.vnet.name
    sensitive = false
}

output "subnet_1_id" {
    value = azurerm_subnet.subnet_1.name
    sensitive = false
}

output "subnet_2_id" {
    value = azurerm_subnet.subnet_2.name
    sensitive = false
}

output "rg_id" {
    value = azurerm_resource_group.rg.name
    sensitive = false
}

output "sa_id" {
    value = azurerm_storage_account.sa.name
    sensitive = false
}
