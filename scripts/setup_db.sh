#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend"
python3 manage.py migrate
python3 ../scripts/seed_data.py --reset
