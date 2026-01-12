terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "7.15.0"
    }
  }
}

provider "google" {
  project = "dtc-de-course-484119"
  region = "europe-west1"
}

resource "google_storage_bucket" "training_bucket" {
  name          = "dtc-de-course-484119-training-bucket"
  location      = "EU"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}