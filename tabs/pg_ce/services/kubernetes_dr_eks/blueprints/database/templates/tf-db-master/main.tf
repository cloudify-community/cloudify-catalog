terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">= 3.20.0"
    }
  }
}

variable "region" {
  type    = string
  default = "eu-west-1"
}

variable "failover" {
  type    = string
  default = "ca-central-1"
}

variable "prefix" {
  type    = string
  default = "xyz"
}

variable "admin_login" {
  type    = string
  default = "cloudify"
}

resource "random_password" "admin_password" {
  length      = 12
  special     = false
  min_lower   = 1
  min_upper   = 1
  min_numeric = 1
}

provider "aws" {
  region = var.region
}

provider "aws" {
  alias   = "failover"
  region  = var.failover
}

data "aws_availability_zones" "primary" {
  provider = aws
}

data "aws_availability_zones" "failover" {
  provider = aws.failover
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.77.0"

  name                 = "${var.prefix}vpc"
  cidr                 = "10.0.0.0/16"
  azs                  = data.aws_availability_zones.primary.names
  public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true

  providers = {

    aws = aws
  }
}

module "vpc_failover" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "2.77.0"

  name                 = "${var.prefix}vpcfailover"
  cidr                 = "10.0.0.0/16"
  azs                  = data.aws_availability_zones.failover.names
  public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  enable_dns_hostnames = true
  enable_dns_support   = true

  providers = {

    aws = aws.failover
  }
}

resource "aws_db_subnet_group" "primary" {
  name       = "${var.prefix}primary"
  subnet_ids = module.vpc.public_subnets

  tags = {
    Name = "Education"
  }
  provider = aws
}

resource "aws_db_subnet_group" "failover" {
  name       = "${var.prefix}failover"
  subnet_ids = module.vpc_failover.public_subnets

  tags = {
    Name = "Education"
  }
  provider = aws.failover
}

resource "aws_rds_global_cluster" "example" {
  global_cluster_identifier = "${var.prefix}-global-dr"
  engine                    = "aurora-postgresql"
  engine_version            = "11.9"
  database_name             = "bulletproof_db"
}

resource "aws_rds_cluster" "primary" {
  provider                  = aws
  engine                    = aws_rds_global_cluster.example.engine
  engine_version            = aws_rds_global_cluster.example.engine_version
  cluster_identifier        = "${var.prefix}-primary-cluster"
  master_username           = var.admin_login
  master_password           = random_password.admin_password.result
  database_name             = "bulletproof_db"
  skip_final_snapshot       = true
  global_cluster_identifier = aws_rds_global_cluster.example.id
  db_subnet_group_name      = "${var.prefix}primary"
  depends_on = [
    aws_db_subnet_group.primary
  ]
}

resource "aws_rds_cluster_instance" "primary" {
  provider             = aws
  engine               = aws_rds_global_cluster.example.engine
  engine_version       = aws_rds_global_cluster.example.engine_version
  identifier           = "${var.prefix}-primary-cluster-instance"
  cluster_identifier   = aws_rds_cluster.primary.id
  instance_class       = "db.r4.large"
  db_subnet_group_name = "${var.prefix}primary"
}

resource "aws_rds_cluster" "failover" {
  provider                  = aws.failover
  engine                    = aws_rds_global_cluster.example.engine
  engine_version            = aws_rds_global_cluster.example.engine_version
  cluster_identifier        = "${var.prefix}-failover-cluster"
  global_cluster_identifier = aws_rds_global_cluster.example.id
  skip_final_snapshot       = true
  db_subnet_group_name      = "${var.prefix}failover"

  depends_on = [
    aws_rds_cluster_instance.primary,
    aws_db_subnet_group.failover
  ]
}

resource "aws_rds_cluster_instance" "failover" {
  provider             = aws.failover
  engine               = aws_rds_global_cluster.example.engine
  engine_version       = aws_rds_global_cluster.example.engine_version
  identifier           = "test-failover-cluster-instance"
  cluster_identifier   = aws_rds_cluster.failover.id
  instance_class       = "db.r4.large"
  db_subnet_group_name = "${var.prefix}failover"
}
