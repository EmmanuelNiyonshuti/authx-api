#!/bin/sh -e
set -x

cd "$(dirname "$0")/../.."

ruff check app --fix
ruff format app
