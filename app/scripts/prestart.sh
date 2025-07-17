#!/bin/sh -e
set -e
set -x

alembic upgrade head

python -m app.seed_db

