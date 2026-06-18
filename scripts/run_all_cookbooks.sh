#!/usr/bin/env bash
# Run all cookbook Python files sequentially and report PASS/FAIL per file.
# Usage: ./scripts/run_all_cookbooks.sh [cookbook_dir_filter]
#
# Examples:
#   ./scripts/run_all_cookbooks.sh             # run all cookbooks
#   ./scripts/run_all_cookbooks.sh 01_agents   # run only 01_agents/*

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
COOKBOOK_DIR="$ROOT/cookbook"
PYTHON="$ROOT/.venvs/demo/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  echo "ERROR: Demo virtualenv not found at $PYTHON"
  echo "Run ./scripts/demo_setup.sh first."
  exit 1
fi

FILTER="${1:-}"

passed=0
failed=0
failed_files=()

while IFS= read -r -d '' file; do
  rel="${file#"$ROOT/"}"

  if [[ -n "$FILTER" && "$file" != *"$FILTER"* ]]; then
    continue
  fi

  printf "Running %-60s ... " "$rel"
  if timeout 120 "$PYTHON" "$file" > /tmp/cookbook_stdout 2>&1; then
    echo "PASS"
    ((passed++))
  else
    echo "FAIL"
    ((failed++))
    failed_files+=("$rel")
    tail -5 /tmp/cookbook_stdout | sed 's/^/  /'
  fi
done < <(find "$COOKBOOK_DIR" -name '*.py' -not -path '*/__pycache__/*' -print0 | sort -z)

echo
echo "Results: $passed passed, $failed failed"
if [[ ${#failed_files[@]} -gt 0 ]]; then
  echo "Failed cookbooks:"
  for f in "${failed_files[@]}"; do
    echo "  - $f"
  done
  exit 1
fi
