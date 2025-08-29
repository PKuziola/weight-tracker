terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "7.0.1"
    }
  }
}

provider "google" {
  project = var.project_id
  credentials = file(var.credentials_file)
}