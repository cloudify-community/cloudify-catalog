terraform {
  required_providers {
    kubernetes = {
      source  = "kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "kubernetes" {
  host                   =  var.cluster_endpoint
  cluster_ca_certificate =  var.cluster_certificate_authority
  token                  =  var.cluster_token
}
