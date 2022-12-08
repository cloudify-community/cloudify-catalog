output "vpc_id" {
  description = "ID of the created VPC"
  value       = module.vpc.vpc_id
}

output "public_subnets" {
  description = "Public subnet IDs"
  value       = module.vpc.public_subnets
}

output "database_subnets" {
  description = "Database subnet IDs"
  value       = module.vpc.database_subnets
}

output "database_subnet_group_name" {
  description = "Database subnet group"
  value       = module.vpc.database_subnet_group_name
}

output "security_group_id" {
  description = "Security Group ID"
  value       = aws_default_security_group.default.id
}

output "private_subnets" {
  description = "Private subnet IDs"
  value       = module.vpc.private_subnets
}

output "private_route_table_ids" {
  description = "IDs of created private route tables"
  value       = module.vpc.private_route_table_ids
}

output "public_route_table_ids" {
  description = "IDs of created public route tables"
  value       = module.vpc.public_route_table_ids
}
