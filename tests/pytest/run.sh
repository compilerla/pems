#!/usr/bin/env bash
set -eu

# run normal pytests
coverage run -m pytest

# clean out old coverage results
rm -rf static/coverage

coverage html --directory static/coverage
