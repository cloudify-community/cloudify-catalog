output "admin_login" {
    value = var.admin_login
    sensitive = false
}

output "admin_password" {
    value = random_password.admin_password.result
    sensitive = true
}

output "db_port" {
    value = aws_rds_cluster.failover.port
    sensitive = false
}

output "db_name" {
    value = aws_rds_cluster.failover.database_name
}

output "endpoint_failover" {
    value = aws_rds_cluster.failover.endpoint
}

output "endpoint_primary" {
    value = aws_rds_cluster.primary.endpoint
}