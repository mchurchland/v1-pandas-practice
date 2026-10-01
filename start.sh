#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v conda >/dev/null 2>&1; then
  printf 'Conda is required. Install Miniconda or Mambaforge, then retry.\n' >&2
  exit 1
fi

if ! conda env list | grep -Eq '^[[:space:]]*v1-pandas-practice[[:space:]]'; then
  conda env create --file environment.yml
fi

exec conda run --no-capture-output -n v1-pandas-practice python -m v1_pandas_practice "$@"
