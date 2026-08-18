#!/usr/bin/env python3
"""Disposable Ordivon Normative conformance witness.

NON-AUTHORITATIVE / NON-CANONICAL / NON-PRODUCTION.

This module executes only explicit fixture semantics. It does not compile domain
rules, select an authoritative current cut, write normative truth, merge
contexts, or authorize operational actions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

FORMAT = "ordivon.normative.conformance.noncanonical-fixture-v1"
SIGNS = {"affirm", "deny"}


class FixtureError(ValueError):
    pass


def _assessment_key(sign: str, claim: str) -> tuple[str, str]:
    if sign not in SIGNS:
        raise FixtureError(f"unsupported sign: {sign!r}")
    if not isinstance(claim, str) or not claim:
        raise FixtureError("claim must be a non-empty opaque string")
    return sign, claim


def _validate_premises(premises: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for premise in premises:
        pid = premise.get("id")
        if not isinstance(pid, str) or not pid:
            raise FixtureError("every premise requires a non-empty id")
        if pid in by_id:
            raise FixtureError(f"duplicate premise id: {pid}")
        kind = premise.get("kind")
        if not isinstance(kind, str) or not kind:
            raise FixtureError(f"premise {pid!r} requires a kind")
        by_id[pid] = premise
    return by_id


def _base_satisfied(
    base: dict[str, Any],
    premise_ids: set[str],
    assessments: set[tuple[str, str]],
) -> tuple[bool, str]:
    if "premise" in base:
        pid = base["premise"]
        return (pid in premise_ids, f"premise:{pid}")
    if "assessment" in base:
        item = base["assessment"]
        key = _assessment_key(item.get("sign"), item.get("claim"))
        return (key in assessments, f"assessment:{key[0]}:{key[1]}")
    raise FixtureError(f"unknown base reference: {base!r}")


def _path_state(
    path: dict[str, Any],
    premise_ids: set[str],
    assessments: set[tuple[str, str]],
) -> dict[str, Any]:
    pid = path.get("id")
    if not isinstance(pid, str) or not pid:
        raise FixtureError("every support path requires a non-empty id")
    sign = path.get("sign")
    claim = path.get("claim")
    _assessment_key(sign, claim)

    bases = path.get("bases", [])
    if not isinstance(bases, list):
        raise FixtureError(f"path {pid!r} bases must be a list")

    missing: list[str] = []
    satisfied: list[str] = []
    for base in bases:
        ok, label = _base_satisfied(base, premise_ids, assessments)
        (satisfied if ok else missing).append(label)

    blockers = path.get("blockedBy", [])
    if not isinstance(blockers, list):
        raise FixtureError(f"path {pid!r} blockedBy must be a list")
    active_blockers = [b for b in blockers if b in premise_ids]

    sufficient = path.get("standingSufficient")
    if not isinstance(sufficient, bool):
        raise FixtureError(f"path {pid!r} requires explicit standingSufficient boolean")

    if missing:
        state = "unsatisfied"
    elif active_blockers:
        state = "blocked"
    elif not sufficient:
        state = "support-only"
    else:
        state = "standing"

    return {
        "id": pid,
        "sign": sign,
        "claim": claim,
        "state": state,
        "standingSufficient": sufficient,
        "satisfiedBases": satisfied,
        "missingBases": missing,
        "activeBlockers": active_blockers,
    }


def evaluate_evaluation(evaluation: dict[str, Any]) -> dict[str, Any]:
    """Evaluate one explicit context/cut fixture.

    The only inference performed is the admitted thin calculus:
    a path can establish its signed claim when all explicit bases are satisfied,
    the path is explicitly standing-sufficient, and no explicit blocker is active.
    Assessment dependencies may form acyclic/multi-step derivations and are
    resolved by monotone fixpoint. Absence never creates a denial.
    """
    context = evaluation.get("context")
    cut = evaluation.get("cut")
    if not isinstance(context, str) or not context:
        raise FixtureError("evaluation requires explicit non-empty context")
    if not isinstance(cut, str) or not cut:
        raise FixtureError("evaluation requires explicit non-empty cut")

    premise_map = _validate_premises(evaluation.get("premises", []))
    premise_ids = set(premise_map)
    paths = evaluation.get("paths", [])
    if not isinstance(paths, list):
        raise FixtureError("paths must be a list")

    path_ids: set[str] = set()
    for path in paths:
        pid = path.get("id")
        if pid in path_ids:
            raise FixtureError(f"duplicate path id: {pid}")
        path_ids.add(pid)

    assessments: set[tuple[str, str]] = set()

    # Monotone fixpoint over explicit assessment dependencies. No rule removal or
    # default negation is performed.
    max_rounds = max(1, len(paths) + 1)
    for _ in range(max_rounds):
        changed = False
        for path in paths:
            trace = _path_state(path, premise_ids, assessments)
            if trace["state"] == "standing":
                key = _assessment_key(trace["sign"], trace["claim"])
                if key not in assessments:
                    assessments.add(key)
                    changed = True
        if not changed:
            break
    else:
        raise FixtureError("fixpoint did not converge within path bound")

    traces = [_path_state(path, premise_ids, assessments) for path in paths]
    rendered_assessments = [
        {"sign": sign, "claim": claim}
        for sign, claim in sorted(assessments, key=lambda x: (x[1], x[0]))
    ]

    return {
        "context": context,
        "cut": cut,
        "assessments": rendered_assessments,
        "paths": traces,
        "premises": list(premise_map.values()),
    }


def check_evaluation(evaluation: dict[str, Any]) -> dict[str, Any]:
    result = evaluate_evaluation(evaluation)
    actual = {(a["sign"], a["claim"]) for a in result["assessments"]}
    expected = evaluation.get("expected", {})

    expected_present = {
        _assessment_key(item.get("sign"), item.get("claim"))
        for item in expected.get("present", [])
    }
    expected_absent = {
        _assessment_key(item.get("sign"), item.get("claim"))
        for item in expected.get("absent", [])
    }
    missing_present = sorted(expected_present - actual)
    forbidden_present = sorted(expected_absent & actual)

    traces = {item["id"]: item for item in result["paths"]}
    path_mismatches: list[dict[str, str]] = []
    for pid, wanted in expected.get("pathStates", {}).items():
        got = traces.get(pid, {}).get("state")
        if got != wanted:
            path_mismatches.append({"path": pid, "expected": wanted, "actual": str(got)})

    passed = not missing_present and not forbidden_present and not path_mismatches
    return {
        "pass": passed,
        "context": result["context"],
        "cut": result["cut"],
        "missingExpected": [
            {"sign": sign, "claim": claim} for sign, claim in missing_present
        ],
        "forbiddenPresent": [
            {"sign": sign, "claim": claim} for sign, claim in forbidden_present
        ],
        "pathMismatches": path_mismatches,
        "result": result,
    }


def check_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    fid = fixture.get("id")
    if not isinstance(fid, str) or not fid:
        raise FixtureError("fixture requires non-empty id")
    evaluations = fixture.get("evaluations", [])
    if not evaluations:
        raise FixtureError(f"fixture {fid} has no evaluations")
    checks = [check_evaluation(item) for item in evaluations]
    return {
        "id": fid,
        "family": fixture.get("family"),
        "title": fixture.get("title"),
        "pass": all(item["pass"] for item in checks),
        "evaluations": checks,
    }


def load_document(path: str | Path) -> dict[str, Any]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("format") != FORMAT:
        raise FixtureError(
            f"fixture document must declare non-canonical format {FORMAT!r}"
        )
    fixtures = data.get("fixtures")
    if not isinstance(fixtures, list):
        raise FixtureError("fixture document requires a fixtures list")
    ids: set[str] = set()
    for fixture in fixtures:
        fid = fixture.get("id")
        if fid in ids:
            raise FixtureError(f"duplicate fixture id: {fid}")
        ids.add(fid)
    return data


def run_document(
    document: dict[str, Any],
    selected: Iterable[str] | None = None,
) -> dict[str, Any]:
    wanted = set(selected or [])
    fixtures = document["fixtures"]
    if wanted:
        known = {item["id"] for item in fixtures}
        missing = sorted(wanted - known)
        if missing:
            raise FixtureError(f"unknown fixture ids: {', '.join(missing)}")
        fixtures = [item for item in fixtures if item["id"] in wanted]

    results = [check_fixture(item) for item in fixtures]
    by_family: dict[str, dict[str, int]] = {}
    for item in results:
        fam = item.get("family") or "UNKNOWN"
        bucket = by_family.setdefault(fam, {"total": 0, "passed": 0, "failed": 0})
        bucket["total"] += 1
        if item["pass"]:
            bucket["passed"] += 1
        else:
            bucket["failed"] += 1

    return {
        "format": FORMAT,
        "pass": all(item["pass"] for item in results),
        "fixtureCount": len(results),
        "passed": sum(bool(item["pass"]) for item in results),
        "failed": sum(not bool(item["pass"]) for item in results),
        "families": by_family,
        "fixtures": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the disposable Ordivon Normative conformance witness."
    )
    parser.add_argument("fixture_document")
    parser.add_argument(
        "--fixture",
        action="append",
        default=[],
        help="Run only this fixture id; repeatable.",
    )
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    try:
        document = load_document(args.fixture_document)
        report = run_document(document, args.fixture)
    except (OSError, json.JSONDecodeError, FixtureError) as exc:
        print(json.dumps({"pass": False, "error": str(exc)}, indent=2))
        return 2

    print(
        json.dumps(
            report,
            indent=None if args.compact else 2,
            separators=(",", ":") if args.compact else None,
            ensure_ascii=False,
        )
    )
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
