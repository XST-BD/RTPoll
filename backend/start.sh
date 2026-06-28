#!/bin/sh
# start.sh
python -m workers.history &
python -m workers.sync & 
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}