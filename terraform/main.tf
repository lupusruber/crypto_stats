# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  credentials = file(var.credentials)
}

resource "google_storage_bucket" "crypto_data_bucket" {
  name                        = var.bucket_name
  location                    = var.region
  force_destroy               = true       # Set to true if you want to be able to delete the bucket even if it contains objects
  storage_class               = "STANDARD" # You can change this to "NEARLINE", "COLDLINE", etc.
  uniform_bucket_level_access = true       # Recommended for simplicity and security

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age = 21 # Deletes objects after 365 days, adjust as needed
    }
  }
}

output "bucket_name" {
  value = google_storage_bucket.crypto_data_bucket.name
}
