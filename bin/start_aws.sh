#!/usr/bin/env bash
set -eu

# S3 bucket name is injected by Copilot as an environment variable
# since it was created via copilot storage init --name pems-db, the variable is 'PEMSDB_NAME'
S3_BUCKET_NAME="$PEMSDB_NAME"
S3_FIXTURE_PATH="fixtures.json"

echo "Downloading $S3_FIXTURE_PATH from bucket $S3_BUCKET_NAME"
aws s3 cp "s3://${S3_BUCKET_NAME}/${S3_FIXTURE_PATH}" "${DJANGO_DB_FIXTURES}"
echo "Download complete"

bin/setup.sh
bin/start.sh
