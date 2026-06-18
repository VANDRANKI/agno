#!/usr/bin/env bash
# Verify that every cookbook directory has a TEST_LOG.md file.
# Exits 1 and lists missing files if any cookbook directory lacks one.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COOKBOOK_DIR="$ROOT/cookbook"

missing=()

while IFS= read -r -d '' dir; do
  # Only top-level cookbook subdirectories (numbered folders like 01_agents/)
  base="$(basename "$dir")"
  if [[ ! "$base" =~ ^[0-9]+ ]]; then
    continue
  fi

  if [[ ! -f "$dir/TEST_LOG.md" ]]; then
    missing+=("${dir#"$ROOT/"}")
  fi
done < <(find "$COOKBOOK_DIR" -maxdepth 1 -mindepth 1 -type d -print0 | sort -z)

if [[ ${#missing[@]} -gt 0 ]]; then
  echo "ERROR: The following cookbook directories are missing TEST_LOG.md:"
  for d in "${missing[@]}"; do
    echo "  - $d"
  done
  exit 1
fi

echo "All cookbook directories have TEST_LOG.md. OK."
