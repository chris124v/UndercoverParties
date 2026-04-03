#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend"
python3 manage.py runserver 8002 --settings=config.settings_localizacion
