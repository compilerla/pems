#!/usr/bin/env bash
set -eux

docker compose build app

docker compose build dev

docker compose build streamlit
