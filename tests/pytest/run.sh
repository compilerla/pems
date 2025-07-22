#!/usr/bin/env bash
set -eu

# clean out old coverage results
rm -rf static/coverage .coverage*

# run normal pytests
coverage run -m pytest

coverage html --directory static/coverage
