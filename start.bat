@echo off
setlocal enabledelayedexpansion

echo Starting NEXUS...
echo.

REM Kill any existing processes on ports 8000 and 5173
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /pid %%a /f 2>nul
for /f "tokens=5" %%a in ('netstat -aon ^| find ":5173" ^| find "LISTENING"') do taskkill /pid %%a /f 2>nul

timeout /t 1 /nobreak

REM Start backend
echo [BACKEND] Starting FastAPI server...
start "NEXUS Backend" cmd /k "cd backend && ..\.venv\Scripts\activate && uvicorn app.main:app --reload --port 8000"

timeout /t 3 /nobreak

REM Start frontend
echo [FRONTEND] Starting Vite dev server...
start "NEXUS Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================
echo NEXUS is starting...
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Close either terminal to stop NEXUS.
echo ============================================
