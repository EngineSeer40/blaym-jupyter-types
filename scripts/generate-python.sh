#!/usr/bin/env bash
# Usage: generate-python.sh [output.py]
# Generates the pydantic models from schema/blaym-jupyter-contracts.schema.json.
set -euo pipefail
cd "$(dirname "$0")/.."
OUT="${1:-python/blaym_jupyter_types/_generated.py}"
.venv/bin/datamodel-codegen \
  --input schema/blaym-jupyter-contracts.schema.json \
  --input-file-type jsonschema \
  --output-model-type pydantic_v2.BaseModel \
  --target-python-version 3.13 \
  --skip-root-model \
  --extra-fields forbid \
  --field-constraints \
  --use-annotated \
  --strict-types str int float bool \
  --disable-timestamp \
  --formatters black isort \
  --custom-file-header "# GENERATED FILE - DO NOT EDIT.
# Source schema: schema/blaym-jupyter-contracts.schema.json (blaym-jupyter-types).
# Regenerate with: npm run python:generate" \
  --output "$OUT"
