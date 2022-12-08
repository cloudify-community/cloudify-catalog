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

resource "google_cloud_tasks_queue" "advanced_configuration" {
  name = "${var.prefix}-cloudify-queue"
  location = var.region

  rate_limits {
    max_concurrent_dispatches = 3
    max_dispatches_per_second = 2
  }

  retry_config {
    max_attempts = 5
    max_retry_duration = "4s"
    max_backoff = "3s"
    min_backoff = "2s"
    max_doublings = 1
  }

  stackdriver_logging_config {
    sampling_ratio = 0.9
  }
}