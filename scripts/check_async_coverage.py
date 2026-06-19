#!/usr/bin/env python3
"""Check that all public async methods have sync counterparts and vice versa.

Run from the repo root:
    python scripts/check_async_coverage.py libs/agno/agno/
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


def collect_method_names(tree: ast.Module) -> tuple[set[str], set[str]]:
    """Return (sync_names, async_names) for all class methods in a module."""
    sync_names: set[str] = set()
    async_names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, ast.AsyncFunctionDef) and not item.name.startswith("_"):
                    async_names.add(item.name)
                elif isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                    sync_names.add(item.name)
    return sync_names, async_names


def check_directory(path: Path) -> list[str]:
    """Return list of violation messages for async/sync coverage gaps."""
    violations: list[str] = []
    for py_file in path.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        sync_names, async_names = collect_method_names(tree)
        for name in async_names:
            if name not in sync_names:
                violations.append(f"{py_file}: async `{name}` has no sync counterpart")
    return violations


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("libs/agno/agno/")
    issues = check_directory(target)
    if issues:
        for issue in issues:
            print(f"MISSING SYNC: {issue}")
        sys.exit(1)
    else:
        print(f"OK: all async methods in {target} have sync counterparts")
