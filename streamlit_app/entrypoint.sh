#!/usr/bin/env bash
set -eux

# Use the value of STREAMLIT_BASE_URL, or a default if it's not set.
BASE_URL_PATH=${STREAMLIT_BASE_URL:-""}

echo "Starting Streamlit with base URL path: /${BASE_URL_PATH}"

# Execute the Streamlit command, passing the base URL path
exec streamlit run streamlit_app/main.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.baseUrlPath="${BASE_URL_PATH}"
