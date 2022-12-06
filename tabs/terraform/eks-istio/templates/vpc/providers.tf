terraform {
  required_providers {
    aws = "~> 3.3"
  }
}

provider "aws" {
  region = var.region
}
