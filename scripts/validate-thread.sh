#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: scripts/validate-thread.sh <thread-markdown-file>"
  exit 1
fi

FILE="$1"

python3 - <<'PY' "$FILE"
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_text(encoding='utf-8')

code_blocks = re.findall(r"```\n(.*?)```", text, re.S)
if len(code_blocks) < 7:
    print(f"FAIL: expected at least 7 code blocks, found {len(code_blocks)}")
    sys.exit(1)

long_lines = []
for idx, block in enumerate(code_blocks, start=1):
    for line_no, line in enumerate(block.splitlines(), start=1):
        stripped = line.strip()
        if stripped and len(stripped) > 20:
            long_lines.append((idx, line_no, stripped))

if long_lines:
    print("WARN: long lines found inside code blocks")
    for slide, line_no, line in long_lines[:20]:
        print(f"  slide {slide} line {line_no}: {line}")

if "http://" in text:
    print("WARN: non-https URL found")

if not re.search(r"https://", text):
    print("WARN: no full URLs found")

print("OK: structural validation finished")
PY
