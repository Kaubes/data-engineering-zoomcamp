variable "project" {
  description = "Project"
  default     = "dtc-de-course-484119"
}

variable "region" {
  description = "Project region"
  default     = "europe-west1"
}

variable "location" {
  description = "Project location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "demo_dataset"
}

variable "gcs_bucket_name" {
  description = "My GCS Bucket Name"
  default     = "dtc-de-course-484119-training-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}