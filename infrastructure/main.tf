

resource "google_bigquery_dataset" "weight_dataset" {
  dataset_id                  = "weight_dataset"  
  description                 = "Dataset containing weight information"
  location                    = var.region
  default_table_expiration_ms = 3600000

  labels = {
    env = "default"
  }
}

resource "google_bigquery_table" "default" {
  dataset_id = google_bigquery_dataset.weight_dataset.dataset_id
  table_id   = "weight"

  deletion_protection = false

  time_partitioning {
    type = "DAY"
  }

  labels = {
    env = "default"
  }

  schema = file("table_schemas/weight_table.json")
}
