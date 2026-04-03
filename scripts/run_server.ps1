$ErrorActionPreference = "Stop"

$Python = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { $Python = "python" }

Set-Location "$PSScriptRoot\..\backend"

& $Python manage.py runserver 8000 --settings=config.settings
