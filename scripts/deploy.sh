#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ./scripts/deploy.sh [--tag TAG] [--suffix SUFFIX] [--no-azure]

Required environment variables:
  DOCKERHUB_USER        Docker Hub username (e.g. goatcatfish)
  AZ_RESOURCE_GROUP     Azure resource group for the Container App
  AZ_CONTAINERAPP_NAME  Azure Container App name

Optional environment variables:
  IMAGE_NAME            Local image name (default: friendbot)
  AZ_SUBSCRIPTION       Azure subscription ID or name
  AZ_REGISTRY_SERVER    Registry server (default: docker.io)

Notes:
  - You must be logged into Docker (docker login).
  - You must be logged into Azure CLI (az login).
EOF
}

TAG=""
SUFFIX=""
NO_AZURE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tag)
      TAG="${2:-}"
      shift 2
      ;;
    --suffix)
      SUFFIX="${2:-}"
      shift 2
      ;;
    --no-azure)
      NO_AZURE=1
      shift 1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

IMAGE_NAME="${IMAGE_NAME:-friendbot}"
DOCKERHUB_USER="${DOCKERHUB_USER:-}"
AZ_RESOURCE_GROUP="${AZ_RESOURCE_GROUP:-}"
AZ_CONTAINERAPP_NAME="${AZ_CONTAINERAPP_NAME:-}"
AZ_SUBSCRIPTION="${AZ_SUBSCRIPTION:-}"
AZ_REGISTRY_SERVER="${AZ_REGISTRY_SERVER:-docker.io}"

if [[ -z "$DOCKERHUB_USER" ]]; then
  echo "DOCKERHUB_USER is required." >&2
  usage
  exit 1
fi

if [[ -z "$TAG" ]]; then
  TAG="$(date +%F)"
  if [[ -n "$SUFFIX" ]]; then
    TAG="${TAG}-${SUFFIX}"
  fi
fi

FULL_IMAGE="${DOCKERHUB_USER}/${IMAGE_NAME}:${TAG}"

echo "Building image: ${IMAGE_NAME}"
docker build -t "${IMAGE_NAME}" .

echo "Tagging image: ${FULL_IMAGE}"
docker tag "${IMAGE_NAME}" "${FULL_IMAGE}"

echo "Pushing image to ${AZ_REGISTRY_SERVER}: ${FULL_IMAGE}"
docker push "${FULL_IMAGE}"

if [[ "$NO_AZURE" -eq 1 ]]; then
  echo "Skipping Azure update (--no-azure)."
  exit 0
fi

if [[ -z "$AZ_RESOURCE_GROUP" || -z "$AZ_CONTAINERAPP_NAME" ]]; then
  echo "AZ_RESOURCE_GROUP and AZ_CONTAINERAPP_NAME are required for Azure update." >&2
  usage
  exit 1
fi

if [[ -n "$AZ_SUBSCRIPTION" ]]; then
  az account set --subscription "$AZ_SUBSCRIPTION"
fi

echo "Updating Azure Container App image to ${FULL_IMAGE}"
az containerapp update \
  --name "$AZ_CONTAINERAPP_NAME" \
  --resource-group "$AZ_RESOURCE_GROUP" \
  --image "$FULL_IMAGE"



