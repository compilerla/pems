#!/usr/bin/env bash
set -eux

# initialize pre-commit
git config --global --add safe.directory /home/$USER/src
pre-commit install --overwrite
