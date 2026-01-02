#!/bin/bash
set -e

# Define temporary database
TEST_DB_FILE="e2e_test_$(date +%s).db"
export DATABASE_URL="sqlite+aiosqlite:///./$TEST_DB_FILE"

echo "Starting E2E tests with database: $TEST_DB_FILE"

# Cleanups
cleanup() {
    echo "Stopping servers..."
    if [ -f backend.pid ]; then
        kill $(cat backend.pid) || true
        rm backend.pid
    fi
    if [ -f frontend.pid ]; then
        pkill -P $(cat frontend.pid) || true
        rm frontend.pid
    fi
    echo "Removing test database..."
    rm -f "$TEST_DB_FILE"
    rm -f backend.log frontend.log
}
trap cleanup EXIT

# 1. Start Backend
echo "Starting Backend..."
# Use python directly to ensure venv usage if active, or assume venv/bin/python
PYTHON_CMD="venv/bin/python"
if [ ! -f "$PYTHON_CMD" ]; then
    PYTHON_CMD="python3"
fi

nohup $PYTHON_CMD -m uvicorn backend.main:app --port 8000 > backend.log 2>&1 &
echo $! > backend.pid

# Wait for Backend to be ready
echo "Waiting for Backend to initialize..."
sleep 5
if ! ps -p $(cat backend.pid) > /dev/null; then
    echo "Backend failed to start. Check backend.log:"
    cat backend.log
    exit 1
fi

# 2. Start Frontend
echo "Starting Frontend..."
cd frontend
BROWSER=none nohup npm start > ../frontend.log 2>&1 &
echo $! > ../frontend.pid
cd ..

# Wait for Frontend to be ready (naive wait, but usually sufficient given create-react-app speed)
echo "Waiting for Frontend to initialize (15s)..."
sleep 15

# 3. Run Tests
echo "Running Pytest..."
# Use venv pytest if available
PYTEST_CMD="venv/bin/pytest"
if [ ! -f "$PYTEST_CMD" ]; then
    PYTEST_CMD="pytest"
fi

$PYTEST_CMD tests/e2e/

echo "E2E Tests Completed Successfully!"
