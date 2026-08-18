from __future__ import annotations

import unittest
from pathlib import Path

from witness import FixtureError, check_evaluation, load_document, run_document


HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures.json"


class WitnessContractTests(unittest.TestCase):
    def test_full_frozen_family_manifest_passes(self) -> None:
        report = run_document(load_document(FIXTURES))
        self.assertTrue(report["pass"])
        self.assertEqual(61, report["fixtureCount"])
        self.assertEqual(
            {"NCX": 16, "NCF": 6, "N3F": 8, "N4F": 7, "N5F": 9, "N6F": 7, "GDF": 8},
            {family: values["total"] for family, values in report["families"].items()},
        )

    def test_missing_cut_fails_closed(self) -> None:
        with self.assertRaises(FixtureError):
            check_evaluation({"context": "C", "premises": [], "paths": [], "expected": {}})

    def test_neither_is_not_denial(self) -> None:
        result = check_evaluation(
            {"context": "C", "cut": "K", "premises": [], "paths": [],
             "expected": {"present": [], "absent": [
                 {"sign": "affirm", "claim": "P"},
                 {"sign": "deny", "claim": "P"},
             ], "pathStates": {}}}
        )
        self.assertTrue(result["pass"])

    def test_both_signs_are_representable(self) -> None:
        result = check_evaluation(
            {"context": "C", "cut": "K",
             "premises": [{"id": "a", "kind": "context"}, {"id": "d", "kind": "context"}],
             "paths": [
                 {"id": "pa", "sign": "affirm", "claim": "P", "bases": [{"premise": "a"}],
                  "standingSufficient": True, "blockedBy": []},
                 {"id": "pd", "sign": "deny", "claim": "P", "bases": [{"premise": "d"}],
                  "standingSufficient": True, "blockedBy": []},
             ],
             "expected": {"present": [
                 {"sign": "affirm", "claim": "P"},
                 {"sign": "deny", "claim": "P"},
             ], "absent": [], "pathStates": {}}}
        )
        self.assertTrue(result["pass"])

    def test_support_only_does_not_assess(self) -> None:
        result = check_evaluation(
            {"context": "C", "cut": "K",
             "premises": [{"id": "a", "kind": "context"}],
             "paths": [
                 {"id": "p", "sign": "affirm", "claim": "P", "bases": [{"premise": "a"}],
                  "standingSufficient": False, "blockedBy": []},
             ],
             "expected": {"present": [], "absent": [{"sign": "affirm", "claim": "P"}],
                          "pathStates": {"p": "support-only"}}}
        )
        self.assertTrue(result["pass"])

    def test_block_does_not_flip_sign(self) -> None:
        result = check_evaluation(
            {"context": "C", "cut": "K",
             "premises": [{"id": "a", "kind": "context"}, {"id": "block", "kind": "context"}],
             "paths": [
                 {"id": "p", "sign": "affirm", "claim": "P", "bases": [{"premise": "a"}],
                  "standingSufficient": True, "blockedBy": ["block"]},
             ],
             "expected": {"present": [], "absent": [
                 {"sign": "affirm", "claim": "P"},
                 {"sign": "deny", "claim": "P"},
             ], "pathStates": {"p": "blocked"}}}
        )
        self.assertTrue(result["pass"])

    def test_multistep_assessment_dependency(self) -> None:
        result = check_evaluation(
            {"context": "C", "cut": "K",
             "premises": [{"id": "s", "kind": "context"}, {"id": "g", "kind": "context"}],
             "paths": [
                 {"id": "status", "sign": "affirm", "claim": "Status(A,S)",
                  "bases": [{"premise": "s"}], "standingSufficient": True, "blockedBy": []},
                 {"id": "permission", "sign": "affirm", "claim": "Permission(A,X)",
                  "bases": [{"assessment": {"sign": "affirm", "claim": "Status(A,S)"}},
                            {"premise": "g"}],
                  "standingSufficient": True, "blockedBy": []},
             ],
             "expected": {"present": [
                 {"sign": "affirm", "claim": "Status(A,S)"},
                 {"sign": "affirm", "claim": "Permission(A,X)"},
             ], "absent": [], "pathStates": {"status": "standing", "permission": "standing"}}}
        )
        self.assertTrue(result["pass"])


if __name__ == "__main__":
    unittest.main()
