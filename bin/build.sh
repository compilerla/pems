#!/usr/bin/env bash
set -eux

docker compose build web

docker compose build dev

docker compose build streamlit
