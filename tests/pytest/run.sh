#!/usr/bin/env bash
set -eu

# run normal pytests
coverage run -m pytest

# clean out old coverage results
rm -rf pems/static/coverage

coverage html --directory pems/static/coverage
