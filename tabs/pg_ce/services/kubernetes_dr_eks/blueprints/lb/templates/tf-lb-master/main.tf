terraform {
  required_providers {
    aws = {
      source                = "hashicorp/aws"
      version               = ">= 3.20.0"
    }
  }
}

provider "aws" {
  region = "us-west-1"

}

variable "domain_primary" {
  type = string
}

variable "domain_failover" {
  type = string
}

variable "domain_owned" {
  type    = string
  default = "aws.com"
}

data "dns_a_record_set" "primary" {
  host = var.domain_primary
}

data "dns_a_record_set" "failover" {
  host = var.domain_failover
}

resource "aws_route53_zone" "primary" {
  name = var.domain_owned
}

resource "aws_route53_health_check" "primary" {
  ip_address        = data.dns_a_record_set.primary.addrs[0]
  port              = 80
  type              = "HTTP"
  resource_path     = "/"
  failure_threshold = "2"
  request_interval  = "30"

  tags = {
    Name = "route53-primary-health-check"
  }
}

resource "aws_route53_health_check" "secondary" {
  ip_address        = data.dns_a_record_set.failover.addrs[0]
  port              = 80
  type              = "HTTP"
  resource_path     = "/"
  failure_threshold = "2"
  request_interval  = "30"

  tags = {
    Name = "route53-secondary-health-check"
  }
}

resource "aws_route53_record" "secondary" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "dr"
  type    = "A"
  ttl     = 10

  failover_routing_policy {
    type = "SECONDARY"
  }

  set_identifier  = "failover"
  records         = [data.dns_a_record_set.failover.addrs[0]]
  health_check_id = aws_route53_health_check.secondary.id
}

resource "aws_route53_record" "primary" {
  zone_id = aws_route53_zone.primary.zone_id
  name    = "dr"
  type    = "A"
  ttl     = 10

  failover_routing_policy {
    type = "PRIMARY"
  }

  set_identifier  = "primary"
  records         = [data.dns_a_record_set.primary.addrs[0]]
  health_check_id = aws_route53_health_check.primary.id
}

output "fqdn_lb" {
  value     = aws_route53_record.primary.fqdn
  sensitive = false
}
