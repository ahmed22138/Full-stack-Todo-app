#!/bin/bash
# Render startup script for TaskFlow API

echo "Starting TaskFlow API..."
uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
