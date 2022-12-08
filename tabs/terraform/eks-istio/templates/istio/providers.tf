terraform {
  required_providers {
    helm = {
      source  = "helm"
      version = "~> 2.0"
    }
    kubernetes = {
      source  = "kubernetes"
      version = "~> 2.0"
    }
  }
}

provider "helm" {
  kubernetes {
    host                   =  var.cluster_endpoint
    cluster_ca_certificate =  var.cluster_certificate_authority
    token                  =  var.cluster_token
  }
}

provider "kubernetes" {
  host                   =  var.cluster_endpoint
  cluster_ca_certificate =  var.cluster_certificate_authority
  token                  =  var.cluster_token
}
