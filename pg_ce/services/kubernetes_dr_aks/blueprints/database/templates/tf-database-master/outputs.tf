output "sql_endpoint" {
  value = azurerm_sql_failover_group.failover.name
  sensitive = false
}

output "admin_password" {
    value = random_password.admin_password.result
    sensitive = true
}

output "admin_login" {
    value = var.admin_login
    sensitive = false
}

output "database_name" {
    value = azurerm_sql_database.db.name
    sensitive = false
}