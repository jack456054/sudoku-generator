provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Artifact Registry Repository
resource "google_artifact_registry_repository" "repo" {
  location      = var.region
  repository_id = var.service_name
  description   = "Docker repository for Sudoku Generator"
  format        = "DOCKER"
}

# 2. Cloud Run Service
resource "google_cloud_run_v2_service" "default" {
  name     = var.service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      # Points to the image in the Artifact Registry create above
      # user must build and push this image before applying the service
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.repo.repository_id}/${var.service_name}:latest"
      
      resources {
        # Allow CPU to be throttled when idle (scale-to-zero cost saving)
        cpu_idle = true
        # Enable startup CPU boost for faster cold starts
        startup_cpu_boost = true

        limits = {
          cpu    = var.cpu_limit
          memory = var.memory_limit
        }
      }
      
      ports {
        container_port = 8080
      }
    }

    scaling {
      # Scale to 0 when not in use
      min_instance_count = 0
      max_instance_count = 5
    }
  }
}

# 3. Allow unauthenticated access (Public)
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_v2_service.default.name
  location = google_cloud_run_v2_service.default.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}
