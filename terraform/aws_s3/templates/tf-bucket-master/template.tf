terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "3.22.0"
    }
  }
}

variable "bucket_region" {
  type = string
  description = "Region to create bucket in"
}

variable "bucket_name" {
  type = string
  description = "Bucket's name"
}

provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "bucket" {
  bucket = var.bucket_name
  acl    = "private"
}
