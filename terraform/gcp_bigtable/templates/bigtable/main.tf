terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.52.0"
    }
  }

  required_version = ">= 0.14"
}

provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = "${var.region}-a"
}

resource "google_bigtable_instance" "instance" {
  name = "${var.prefix}-bt-instance"
  cluster {
    cluster_id   = "${var.prefix}-bt-instance-cluster"
    zone         = "${var.region}-a"
    num_nodes    = 3
    storage_type = "SSD"
  }

  instance_type = "PRODUCTION"
  deletion_protection  = "true"
}