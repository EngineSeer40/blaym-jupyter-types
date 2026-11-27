#!/usr/bin/env bash
# Regenerates to a temp file and fails if it differs from the committed models.
set -euo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
scripts/generate-python.sh "$TMP/_generated.py"
if ! diff -u python/blaym_notebook_types/_generated.py "$TMP/_generated.py"; then
  echo "python models drift: run 'npm run python:generate'" >&2
  exit 1
fi
echo "python models up to date"
