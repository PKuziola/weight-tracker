variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "pk-project-470517"
}

variable "credentials_file" {
  description = "Path to the GCP service account key file"
  type        = string  
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-central2"
}
