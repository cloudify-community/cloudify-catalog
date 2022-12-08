terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=3.52.0"
    }
  }

  required_version = ">= 0.14"
}

provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = "${var.region}-a"
}

resource "google_compute_disk" "default" {
  name  = "${var.prefix}-cloudify-disk"
  type  = "pd-ssd"
  zone  = "${var.region}-a"
  labels = {
    environment = "dev"
  }
  physical_block_size_bytes = 4096
}