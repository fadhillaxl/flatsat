#!/bin/bash
trap "kill 0" EXIT

echo "Starting Backend..."
source backend/.venv/bin/activate
python -m backend.main &

echo "Starting Frontend..."
cd frontend
npm run dev &

wait
