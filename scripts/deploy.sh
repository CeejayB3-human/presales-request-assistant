#!/usr/bin/env bash
# Deploys the stack and uploads the service catalog PDF.
# Run from the repository root, e.g. in AWS CloudShell (SAM CLI and AWS CLI are preinstalled).
#
# Usage: ./scripts/deploy.sh [stack-name] [model-id]
set -euo pipefail

STACK_NAME="${1:-presales-request-assistant}"
MODEL_ID="${2:-us.anthropic.claude-sonnet-5}"
REGION="${AWS_REGION:-us-east-1}"
CATALOG_FILE="catalog/IT_Service_Catalog.pdf"

echo "Deploying stack '$STACK_NAME' to $REGION with model $MODEL_ID ..."
sam deploy \
  --template-file template.yaml \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --resolve-s3 \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset \
  --no-fail-on-empty-changeset \
  --parameter-overrides "ModelId=$MODEL_ID"

output() {
  aws cloudformation describe-stacks --stack-name "$STACK_NAME" --region "$REGION" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text
}

BUCKET="$(output CatalogBucketName)"
URL="$(output DemoUrl)"

echo "Uploading $CATALOG_FILE to s3://$BUCKET/ ..."
aws s3 cp "$CATALOG_FILE" "s3://$BUCKET/IT_Service_Catalog.pdf" --region "$REGION"

echo
echo "Done. Open: $URL"
