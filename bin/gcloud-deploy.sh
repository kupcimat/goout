#!/bin/zsh

set -ex

GCP_PROJECT_ID=$1
GCP_IMAGE_NAME=gcr.io/${GCP_PROJECT_ID}/backend

# Authenticate to container registry
gcloud auth configure-docker gcr.io

# Build image locally using docker
docker build . --tag ${GCP_IMAGE_NAME}

# Push image to container registry
docker push ${GCP_IMAGE_NAME}

# Deploy server on gcloud
gcloud run deploy backend-service --image ${GCP_IMAGE_NAME} --platform managed
