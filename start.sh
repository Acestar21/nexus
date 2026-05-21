#!/bin/bash

echo "Starting NEXUS..."
echo ""

# Kill existing processes
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:5173 | xargs kill -9 2>/dev/null || true

sleep 1

# Start backend
cd backend
echo "[BACKEND] Starting FastAPI server..."
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

sleep 3

# Start frontend
cd frontend
echo "[FRONTEND] Starting Vite dev server..."
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "============================================"
echo "NEXUS is starting..."
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop NEXUS."
echo "============================================"
echo ""

# Wait for both processes
wait