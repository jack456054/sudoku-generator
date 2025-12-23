variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "The GCP region to deploy to"
  type        = string
  default     = "asia-east1"
}

variable "service_name" {
  description = "The name of the Cloud Run service"
  type        = string
  default     = "sudoku-generator"
}

variable "cpu_limit" {
  description = "CPU limit for the container"
  type        = string
  default     = "1000m"
}

variable "memory_limit" {
  description = "Memory limit for the container"
  type        = string
  default     = "512Mi"
}
