#!/usr/bin/env bash
set -euo pipefail

if [[ $# -gt 0 ]]; then
  echo "Do not pass auth tokens as CLI arguments. Pipe via stdin or use interactive login." >&2
  exit 1
fi

if [[ -t 0 ]]; then
  xactions login
else
  xactions login < /dev/stdin
fi
