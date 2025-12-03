#!/usr/bin/env bash
set -euo pipefail

# Allow overriding ports from env
API_HOST="${API_HOST:-0.0.0.0}"
API_PORT="${API_PORT:-8000}"
STREAMLIT_HOST="${STREAMLIT_HOST:-0.0.0.0}"
STREAMLIT_PORT="${STREAMLIT_PORT:-8501}"

# Optional: print a quick banner
echo "Starting FastAPI on ${API_HOST}:${API_PORT} and Streamlit on ${STREAMLIT_HOST}:${STREAMLIT_PORT}"

# Start uvicorn in background
# Use --loop=auto and --workers 1 by default; increase workers if you know CPU needs
uvicorn app:app --host "${API_HOST}" --port "${API_PORT}" --workers 1 &

UVICORN_PID=$!

# Trap signals to forward to uvicorn, ensuring graceful shutdown
_term() {
  echo "Caught SIGTERM, stopping uvicorn (${UVICORN_PID})"
  kill -TERM "${UVICORN_PID}" 2>/dev/null || true
  wait "${UVICORN_PID}" || true
  exit 0
}
trap _term SIGTERM SIGINT

# Start streamlit in foreground so container stays alive; adjust path if your streamlit entry is different
# e.g. if your main streamlit file is frontend/app.py change accordingly
streamlit run frontend/st_app.py --server.address "${STREAMLIT_HOST}" --server.port "${STREAMLIT_PORT}"

# Wait for uvicorn if streamlit ever exits
wait "${UVICORN_PID}"