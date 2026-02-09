@echo off
echo Starting RAG Document Q&A System...
echo.

echo Starting Backend Server...
start cmd /k "cd backend && echo Backend starting on http://localhost:8000 && python main.py"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start cmd /k "cd RAG_ && echo Frontend starting... && npm run dev"

echo.
echo Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this window...
pause > nul
