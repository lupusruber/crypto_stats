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
  force_destroy               = true
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }

    condition {
      age = 21
    }
  }
}

resource "google_bigquery_dataset" "crypto_stats" {
  dataset_id = "crypto_stats"
  project     = var.project_id
}

output "bucket_name" {
  value = google_storage_bucket.crypto_data_bucket.name
}
