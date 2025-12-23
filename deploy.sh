#!/bin/bash
set -e

# Usage: ./deploy.sh <PROJECT_ID> [REGION]

if [ -z "$1" ]; then
    echo "Usage: ./deploy.sh <PROJECT_ID> [REGION]"
    exit 1
fi

PROJECT_ID=$1
REGION=${2:-asia-east1}
SERVICE_NAME="sudoku-generator"

echo "Deploying to Project: $PROJECT_ID, Region: $REGION"

# 1. Prepare GCS Backend for Terraform State
BUCKET_NAME="tf-state-$PROJECT_ID"
echo "Verifying State Bucket: $BUCKET_NAME..."

if ! gcloud storage buckets describe "gs://$BUCKET_NAME" --project "$PROJECT_ID" > /dev/null 2>&1; then
    echo "Creating bucket $BUCKET_NAME..."
    gcloud storage buckets create "gs://$BUCKET_NAME" --project "$PROJECT_ID" --location "$REGION" --uniform-bucket-level-access
else
    echo "Bucket $BUCKET_NAME already exists."
fi

# 2. Initialize Terraform with Remote Backend
echo "Initializing Terraform..."
cd terraform
# We use partial configuration to pass the bucket name dynamically
terraform init \
    -migrate-state \
    -force-copy \
    -backend-config="bucket=$BUCKET_NAME" \
    -backend-config="prefix=sudoku-generator"

# 2. Create Artifact Registry (Targeted Apply)
echo "Ensuring Artifact Registry exists..."
terraform apply -target=google_artifact_registry_repository.repo \
    -var="project_id=$PROJECT_ID" \
    -var="region=$REGION" \
    -auto-approve

# 3. Build and Push Docker Image
REPO_URL="$REGION-docker.pkg.dev/$PROJECT_ID/$SERVICE_NAME/$SERVICE_NAME"
echo "Building and Pushing Image to $REPO_URL..."

# Enable Artifact Registry API usually required for build
# gcloud services enable artifactregistry.googleapis.com --project $PROJECT_ID

cd ..
gcloud builds submit --tag "$REPO_URL:latest" --project "$PROJECT_ID" .

# 4. Deploy Cloud Run Service (Full Apply)
echo "Deploying Cloud Run Service..."
cd terraform
terraform apply \
    -var="project_id=$PROJECT_ID" \
    -var="region=$REGION" \
    -auto-approve

echo "Deployment Complete!"
terraform output service_url
