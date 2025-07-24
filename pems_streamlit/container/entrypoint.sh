#!/usr/bin/env bash
set -eux

# Use the value of STREAMLIT_BASE_URL, or the root path if it's not set.
BASE_URL_PATH=${STREAMLIT_BASE_URL:-""}

echo "Starting Streamlit with base URL path: ${BASE_URL_PATH}"

# Execute the Streamlit command, passing the base URL path
# Use the run.py helper since streamlit run wants the path to a python file
exec streamlit run run.py \
  --server.port=8501 \
  --server.address=0.0.0.0 \
  --server.baseUrlPath="${BASE_URL_PATH}"
