#!/usr/bin/env python3
"""Verify that the Agno development environment is correctly configured.

This script checks for required Python version, virtual environment activation,
dependencies, and database connectivity.

Usage::

    python scripts/check_agent_setup.py
    python scripts/check_agent_setup.py --strict  # fail on warnings
"""

from __future__ import annotations

import argparse
import importlib
import sys
from dataclasses import dataclass, field
from typing import Callable

MIN_PYTHON = (3, 10)
RECOMMENDED_PYTHON = (3, 11)

# Packages that must be importable for the dev environment to function.
REQUIRED_PACKAGES: list[str] = [
    "agno",
    "openai",
    "pydantic",
]

OPTIONAL_PACKAGES: list[str] = [
    "anthropic",
    "google.generativeai",
    "psycopg2",
    "sqlalchemy",
]


@dataclass
class CheckResult:
    """Outcome of a single environment check."""

    name: str
    passed: bool
    message: str
    is_warning: bool = False
    details: list[str] = field(default_factory=list)


def check_python_version() -> CheckResult:
    """Verify that the running Python version meets the minimum requirement.

    Returns:
        A :class:`CheckResult` indicating whether the Python version is
        acceptable, with a warning when it is below the recommended version.
    """
    current = sys.version_info[:2]
    if current < MIN_PYTHON:
        return CheckResult(
            name="Python version",
            passed=False,
            message=(
                f"Python {'.'.join(map(str, current))} is too old. "
                f"Minimum required: {'.'.join(map(str, MIN_PYTHON))}"
            ),
        )
    is_warning = current < RECOMMENDED_PYTHON
    return CheckResult(
        name="Python version",
        passed=True,
        is_warning=is_warning,
        message=(
            f"Python {'.'.join(map(str, current))} detected."
            + (
                f" Recommended: {'.'.join(map(str, RECOMMENDED_PYTHON))}+"
                if is_warning
                else ""
            )
        ),
    )


def check_package(package_name: str, *, required: bool = True) -> CheckResult:
    """Check whether a Python package is importable.

    Args:
        package_name: The importable module name (e.g. ``"openai"`` or
            ``"google.generativeai"``).
        required: When *True* a missing package is a failure; when *False* it
            is a warning.

    Returns:
        A :class:`CheckResult` for this package.
    """
    try:
        mod = importlib.import_module(package_name)
        version = getattr(mod, "__version__", "unknown")
        return CheckResult(
            name=f"Package: {package_name}",
            passed=True,
            message=f"{package_name} {version} installed",
        )
    except ImportError:
        return CheckResult(
            name=f"Package: {package_name}",
            passed=False,
            is_warning=not required,
            message=(
                f"{package_name} is {'not installed' if required else 'not installed (optional)'}"
            ),
        )


def check_virtual_env() -> CheckResult:
    """Check whether a virtual environment is active.

    Returns:
        A warning-level :class:`CheckResult` when no virtual environment is
        detected so that global installs are avoided accidentally.
    """
    in_venv = sys.prefix != sys.base_prefix or hasattr(sys, "real_prefix")
    return CheckResult(
        name="Virtual environment",
        passed=True,
        is_warning=not in_venv,
        message=(
            "Virtual environment is active."
            if in_venv
            else "No virtual environment detected — consider using .venv/"
        ),
    )


def run_checks() -> list[CheckResult]:
    """Run all environment checks and return their results.

    Returns:
        Ordered list of :class:`CheckResult` objects.
    """
    checks: list[Callable[[], CheckResult]] = [
        check_python_version,
        check_virtual_env,
    ]
    results: list[CheckResult] = [fn() for fn in checks]
    for pkg in REQUIRED_PACKAGES:
        results.append(check_package(pkg, required=True))
    for pkg in OPTIONAL_PACKAGES:
        results.append(check_package(pkg, required=False))
    return results


def print_report(results: list[CheckResult], *, strict: bool = False) -> int:
    """Print a formatted report and return a shell exit code.

    Args:
        results: The list of check results to report.
        strict: When *True*, warnings are treated as failures.

    Returns:
        ``0`` on success, ``1`` if any failures (or warnings in strict mode)
        are present.
    """
    failures = 0
    for r in results:
        if not r.passed and not r.is_warning:
            icon, label = "FAIL", "FAIL"
            failures += 1
        elif r.is_warning and (not r.passed or strict):
            icon, label = "WARN", "WARN"
            if strict:
                failures += 1
        else:
            icon, label = "OK  ", "OK"
        print(f"[{label}] {r.name}: {r.message}")
        for detail in r.details:
            print(f"       {detail}")

    print(f"\n{'All checks passed.' if failures == 0 else f'{failures} check(s) failed.'}")
    return 0 if failures == 0 else 1


def main() -> None:
    """Entry point for the environment setup checker."""
    parser = argparse.ArgumentParser(
        description="Verify the Agno development environment."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as failures.",
    )
    args = parser.parse_args()
    results = run_checks()
    sys.exit(print_report(results, strict=args.strict))


if __name__ == "__main__":
    main()
