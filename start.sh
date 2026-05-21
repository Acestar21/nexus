#!/bin/bash

set -e

echo "Starting NEXUS..."
echo ""

# Ensure script is executed from repository root
if [ ! -f ".env.example" ]; then
    echo "[ERROR] Please run start.sh from the NEXUS repository root."
    exit 1
fi

# Ensure virtual environment exists
if [ ! -d ".venv" ]; then
    echo "[ERROR] Virtual environment not found."
    echo "Create it with:"
    echo "python -m venv .venv"
    exit 1
fi

# Ensure frontend dependencies exist
if [ ! -d "frontend/node_modules" ]; then
    echo "[ERROR] Frontend dependencies not installed."
    echo "Run:"
    echo "cd frontend && npm install"
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Check Ollama
if ! command -v ollama &> /dev/null; then
    echo "[WARNING] Ollama is not installed or not in PATH."
fi

# Kill existing local dev ports
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

sleep 1

# Start backend
echo "[BACKEND] Starting FastAPI server..."
cd backend
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

sleep 3

# Start frontend
echo "[FRONTEND] Starting Vite dev server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "============================================"
echo "NEXUS is running"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop NEXUS."
echo "============================================"
echo ""

# Cleanup on exit
cleanup() {
    echo ""
    echo "Stopping NEXUS..."

    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true

    exit 0
}

trap cleanup SIGINT SIGTERM

wait