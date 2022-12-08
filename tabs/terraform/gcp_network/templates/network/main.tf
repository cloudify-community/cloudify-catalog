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

resource "google_compute_subnetwork" "network-with-private-secondary-ip-ranges" {
  name          = "${var.prefix}-subnetwork"
  ip_cidr_range = "10.2.0.0/16"
  region        = var.region
  network       = google_compute_network.network.id
  secondary_ip_range {
    range_name    = "${var.prefix}-tf-test-secondary-range"
    ip_cidr_range = "192.168.10.0/24"
  }
}

resource "google_compute_network" "network" {
  name                    = "${var.prefix}-network"
  auto_create_subnetworks = false
}