#!/bin/bash
echo "Restarting local backend..."
pkill -f "uvicorn backend.main:app" || echo "No local uvicorn found."
nohup ./venv/bin/uvicorn backend.main:app --reload --port 8000 > backend_local.log 2>&1 &
echo "Local backend started with --reload on port 8000."
