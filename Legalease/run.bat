@echo off
title LegalEase - AI Legal Document Generator

echo ===================================================
echo Starting LegalEase Backend (FastAPI on Port 8000)...
echo ===================================================
start "LegalEase Backend" cmd /k "python -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo Waiting 2 seconds for backend initialization...
timeout /t 2 /nobreak >nul

echo ===================================================
echo Starting LegalEase Frontend (Streamlit on Port 8501)...
echo ===================================================
python -m streamlit run frontend/app.py --server.port 8501
pause
