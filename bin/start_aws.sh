#!/usr/bin/env bash
set -eu

# S3 bucket name (BUCKET_NAME) is injected by Copilot as an environment variable
# in the service manifest
S3_FIXTURE_PATH="fixtures.json"

echo "Downloading $S3_FIXTURE_PATH from bucket $BUCKET_NAME"
aws s3 cp "s3://${BUCKET_NAME}/${S3_FIXTURE_PATH}" "${DJANGO_DB_FIXTURES}"
echo "Download complete"

bin/setup.sh
bin/start.sh
