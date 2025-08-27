@echo off
echo ========================================
echo Starting DVM Scoring Engine
echo ========================================

REM Kill any existing processes
echo Stopping any existing servers...
taskkill /F /IM uvicorn.exe 2>NUL
taskkill /F /IM python.exe /FI "WINDOWTITLE eq uvicorn*" 2>NUL
timeout /t 2 /nobreak >NUL

REM Start backend
echo.
echo Starting backend server...
start "DVM Backend" cmd /k ".venv\Scripts\activate && python -m uvicorn app.api.server:app --reload --port 8000 --host 127.0.0.1"

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak >NUL

REM Start frontend
echo.
echo Starting frontend server...
cd frontend
start "DVM Frontend" cmd /k "npm run dev -- -p 4000"
cd ..

echo.
echo ========================================
echo Project started successfully!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:4000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >NUL
