#!/usr/bin/env bash
# Setup a local development virtualenv and install dependencies.
# Usage: ./scripts/setup_dev.sh

set -euo pipefail

PYTHON=${1:-python3}
VENV_DIR=.venv

echo "Using Python: $(which $PYTHON)"

if [ -d "$VENV_DIR" ]; then
  echo "Virtualenv $VENV_DIR already exists. Activate it with: source $VENV_DIR/bin/activate"
  exit 0
fi

echo "Creating virtualenv in $VENV_DIR..."
$PYTHON -m venv $VENV_DIR

echo "Activating virtualenv and upgrading pip..."
source $VENV_DIR/bin/activate
python -m pip install --upgrade pip

if [ -f requirements.txt ]; then
  echo "Installing runtime requirements..."
  pip install -r requirements.txt
fi

if [ -f requirements-dev.txt ]; then
  echo "Installing development requirements..."
  pip install -r requirements-dev.txt
fi

echo "Development environment is ready. Activate with: source $VENV_DIR/bin/activate"
