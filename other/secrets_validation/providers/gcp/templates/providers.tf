terraform {
  required_providers {
    google = {
      version = "~> 3.83.0"
    }
  }
}

provider "google" {
  project     = var.project_name
  region      = var.region
}