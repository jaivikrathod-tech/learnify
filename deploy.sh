#!/bin/bash
set -e

echo "=== IALA Google Cloud Run Deployment ==="

# 1. Project Configuration
PROJECT_ID=$(gcloud config get-value project)
REGION="us-central1"

if [ -z "$PROJECT_ID" ]; then
    echo "No active Google Cloud project found."
    exit 1
fi


# Set the active project
gcloud config set project "$PROJECT_ID"

# Enable necessary APIs
echo "Enabling necessary Google Cloud APIs..."
gcloud services enable run.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com

# 2. Artifact Registry Setup
REPO_NAME="iala-repo"
echo "Checking if Artifact Registry repository '$REPO_NAME' exists..."
if ! gcloud artifacts repositories describe "$REPO_NAME" --location="$REGION" >/dev/null 2>&1; then
    echo "Creating repository '$REPO_NAME'..."
    gcloud artifacts repositories create "$REPO_NAME" \
        --repository-format=docker \
        --location="$REGION" \
        --description="Docker repository for IALA services"
fi

BACKEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/iala-backend"
FRONTEND_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/iala-frontend"

# 3. Deploy Backend
echo "--- Deploying Backend ---"
cd iala
echo "Building backend image using Cloud Build..."
gcloud builds submit --tag "$BACKEND_IMAGE" .

echo "Deploying backend to Cloud Run..."
# Note: For MVP, using sqlite so no DATABASE_URL provided yet. 
# For production Postgres, add: --set-env-vars DATABASE_URL="postgresql://user:pass@host/db"
gcloud run deploy iala-backend \
    --image "$BACKEND_IMAGE" \
    --region "$REGION" \
    --allow-unauthenticated \
    --port 8080

# Retrieve backend URL
BACKEND_URL=$(gcloud run services describe iala-backend --region "$REGION" --format 'value(status.url)')
echo "Backend deployed at: $BACKEND_URL"
cd ..

# 4. Deploy Frontend
echo "--- Deploying Frontend ---"
cd iala-frontend
echo "Building frontend image using Cloud Build..."
gcloud builds submit --tag "$FRONTEND_IMAGE" .

echo "Deploying frontend to Cloud Run..."
gcloud run deploy iala-frontend \
    --image "$FRONTEND_IMAGE" \
    --region "$REGION" \
    --allow-unauthenticated \
    --port 8080 \
    --set-env-vars="BACKEND_URL=$BACKEND_URL"

# Retrieve frontend URL
FRONTEND_URL=$(gcloud run services describe iala-frontend --region "$REGION" --format 'value(status.url)')
echo "Frontend deployed at: $FRONTEND_URL"
cd ..

echo "=== Deployment Complete! ==="
echo "Access your app at: $FRONTEND_URL"
