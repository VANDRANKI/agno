#!/usr/bin/env python3
"""Lint cookbook directories for structural compliance.

Checks that every cookbook directory has README.md and TEST_LOG.md,
and that Python example files contain a module-level docstring.

Usage:
    python scripts/lint_cookbooks.py
    python scripts/lint_cookbooks.py --strict   # fail on any warning
"""
from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

COOKBOOK_ROOT = Path("cookbook")
REQUIRED_FILES = {"README.md", "TEST_LOG.md"}


def has_module_docstring(py_file: Path) -> bool:
    """Return True if the Python file starts with a module docstring."""
    try:
        tree = ast.parse(py_file.read_text(encoding="utf-8"))
    except SyntaxError:
        return False
    return (
        bool(tree.body)
        and isinstance(tree.body[0], ast.Expr)
        and isinstance(tree.body[0].value, ast.Constant)
        and isinstance(tree.body[0].value.value, str)
    )


def lint_directory(directory: Path) -> list[str]:
    """Return list of lint issues for a single cookbook directory."""
    issues: list[str] = []
    existing = {f.name for f in directory.iterdir() if f.is_file()}
    for required in sorted(REQUIRED_FILES):
        if required not in existing:
            issues.append(f"Missing required file: {required}")
    for py_file in sorted(directory.glob("*.py")):
        if not has_module_docstring(py_file):
            issues.append(f"{py_file.name}: missing module-level docstring")
    return issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict", action="store_true",
        help="Exit non-zero even for warnings"
    )
    parser.add_argument(
        "--path", type=Path, default=COOKBOOK_ROOT,
        help=f"Cookbook root directory (default: {COOKBOOK_ROOT})",
    )
    args = parser.parse_args(argv)

    root: Path = args.path
    if not root.exists():
        print(f"ERROR: {root} does not exist.", file=sys.stderr)
        return 1

    all_issues: dict[str, list[str]] = {}
    checked = 0
    for item in sorted(root.iterdir()):
        if not item.is_dir() or item.name.startswith("."):
            continue
        checked += 1
        issues = lint_directory(item)
        if issues:
            all_issues[item.name] = issues

    if all_issues:
        print(f"Lint issues found in {len(all_issues)}/{checked} directories:\n")
        for dirname, issues in sorted(all_issues.items()):
            for issue in issues:
                print(f"  {dirname}/{issue}")
        return 1

    print(f"All {checked} cookbook directories passed lint checks.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
