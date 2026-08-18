#!/usr/bin/env python3
"""Compact full-regression runner for the non-authoritative conformance witness."""

from __future__ import annotations

import json
from pathlib import Path

from witness import load_document, run_document


HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures.json"


def main() -> int:
    report = run_document(load_document(FIXTURES))
    summary = {
        "pass": report["pass"],
        "fixtureCount": report["fixtureCount"],
        "passed": report["passed"],
        "failed": report["failed"],
        "families": report["families"],
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    if not report["pass"]:
        for fixture in report["fixtures"]:
            if not fixture["pass"]:
                print(json.dumps(fixture, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
