#!/bin/bash
# Startup script for LegalEase (FastAPI backend + Streamlit frontend)

echo "Starting LegalEase Backend (FastAPI)..."
python -m uvicorn legalEaseAPI.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo "Starting LegalEase Frontend (Streamlit)..."
streamlit run frontend/app.py --server.port 8501

kill $BACKEND_PID
