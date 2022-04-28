terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=3.52.0"
    }
  }

  required_version = ">= 0.14"
}

variable "prefix" {
    type = string
    default = "xyz"
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "project_id" {
  type    = string
  default = "cloudify-cs"
}

variable "root_password" {
  type    = string
  default = "P@ssw0rd1234!"
}

variable "database_name" {
  type    = string
  default = "cloudify"
}

variable "user_name" {
  type    = string
  default = "cloudify_user"
}

variable "user_password" {
  type    = string
  default = "P@ssw0rd1234!"
}
provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = "${var.region}-a"
}

resource "google_cloud_run_service" "default" {
  name     = "${var.prefix}-postgresql"
  location = var.region

  template {
    spec {
      containers {
        ports {
          container_port = 5432
        }
        image = "marketplace.gcr.io/google/POSTGRESQL5"
        env {
          name  = "POSTGRES_PASSWORD"
          value = var.user_password
        }

      }
    }
  }
}
