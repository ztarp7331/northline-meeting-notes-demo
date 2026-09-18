#!/usr/bin/env bash
# One-command free demo: venv + install + sample preview (no API key needed).
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "Error: python3 not found. Install Python 3.10+ and retry." >&2
  exit 1
fi

if [ ! -d .venv ]; then
  echo "==> Creating virtualenv (.venv)"
  "$PYTHON" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Installing dependencies"
pip install -q -r requirements.txt

echo ""
echo "==> Sample output (no API call) — run with your key for a live result"
echo "    See README.md for: python main.py examples/sample_meeting_notes.txt"
echo "    Or UI:            python app.py"
echo ""
python main.py --show-sample
