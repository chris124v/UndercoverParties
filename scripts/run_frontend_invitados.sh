#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend"
python3 manage.py runserver 8001 --settings=config.settings_invitados
