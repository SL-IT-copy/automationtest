#!/usr/bin/env bash
set -euo pipefail

export PUPPETEER_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

xactions profile "$@"
