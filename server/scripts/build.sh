#!/bin/bash
set -e

TARGET_PYTHON_VERSION="3.11"
TARGET_PLATFORM="x86_64-manylinux2014"
TARGET_DIST_DIR="packages"

uv export --frozen --no-dev --no-editable --no-hashes --quiet -o requirements.txt

rm -rf "$TARGET_DIST_DIR"
mkdir -p "$TARGET_DIST_DIR"

uv pip install \
  --no-installer-metadata \
  --no-compile-bytecode \
  --python-platform "$TARGET_PLATFORM" \
  --python "$TARGET_PYTHON_VERSION" \
  --target "$TARGET_DIST_DIR" \
  --quiet \
  -r requirements.txt

rm -f "$TARGET_DIST_DIR.zip"

cp -r src "$TARGET_DIST_DIR"
cd "$TARGET_DIST_DIR"
zip -rq "../$TARGET_DIST_DIR.zip" .
