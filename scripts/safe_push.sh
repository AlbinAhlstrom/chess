#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")/.."

echo "Running full test suite..."

# Run tests using the virtual environment's pytest
# Assuming venv is in the project root
if [ -f "./venv/bin/pytest" ]; then
    ./venv/bin/pytest
else
    echo "Error: Virtual environment pytest not found at ./venv/bin/pytest"
    exit 1
fi

# Check exit code of pytest
if [ $? -eq 0 ]; then
    echo "Tests passed! Pushing to remote..."
    git push
else
    echo "Tests failed. Push aborted."
    exit 1
fi
