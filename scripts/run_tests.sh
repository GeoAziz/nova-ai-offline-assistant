#!/usr/bin/env bash
# Run the test suite using the project's virtualenv if present.
# Usage: ./scripts/run_tests.sh

set -euo pipefail

VENV_DIR=.venv

if [ -d "$VENV_DIR" ]; then
  echo "Activating virtualenv $VENV_DIR"
  # shellcheck disable=SC1091
  source $VENV_DIR/bin/activate
fi

echo "Running unit tests (unittest discovery)..."
python -m unittest discover -v

echo "Running flake8..."
if command -v flake8 >/dev/null 2>&1; then
  flake8
else
  echo "flake8 not found. To run linters, install dev deps: ./scripts/setup_dev.sh"
fi
