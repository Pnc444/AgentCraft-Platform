#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_PORT="${BACKEND_PORT:-8001}"
FRONTEND_PORT="${FRONTEND_PORT:-3001}"

cleanup() {
  if [[ -n "${BACKEND_PID:-}" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

cd "$ROOT/backend"
if [[ ! -d .venv ]]; then
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements/development.txt
else
  source .venv/bin/activate
fi

python manage.py migrate --noinput
python manage.py seed_demo

python manage.py runserver "0.0.0.0:${BACKEND_PORT}" &
BACKEND_PID=$!

cd "$ROOT/frontend"
npm install
NEXT_PUBLIC_API_URL="http://localhost:${BACKEND_PORT}/api/v1" \
  INTERNAL_API_URL="http://localhost:${BACKEND_PORT}" \
  npm run dev -- --hostname 0.0.0.0 --port "${FRONTEND_PORT}"
