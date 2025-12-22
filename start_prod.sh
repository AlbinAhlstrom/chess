#!/bin/bash
# Install dependencies
pip install -r requirements.txt
# Start the server on port 8000
nohup uvicorn backend.main:app --host 0.0.0.0 --port 8000 > backend.log 2>&1 &
echo "Backend started in background. Logs are in backend.log"
