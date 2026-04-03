#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend"
python3 manage.py runserver 8000 --settings=config.settings
