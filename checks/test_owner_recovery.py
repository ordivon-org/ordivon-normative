from __future__ import annotations

import hashlib
import json
import subprocess
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
OWNER = "research-owner:ordivon-normative"
AUTHORITY = "authority:ordivon:research-owner:ordivon-normative"


def _load(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"{path} must contain an object")
    return value


def _relative_file(value: object) -> Path:
    if not isinstance(value, str) or not value or value != value.strip():
        raise AssertionError(f"invalid relative path: {value!r}")
    pure = PurePosixPath(value)
    if pure.is_absolute() or ".." in pure.parts:
        raise AssertionError(f"path escapes owner root: {value}")
    path = ROOT.joinpath(*pure.parts)
    if not path.is_file():
        raise AssertionError(f"owner recovery path is missing: {value}")
    return path


class NormativeOwnerRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.current = _load(ROOT / "authority" / "CURRENT.json")
        cls.publication_path = _relative_file(cls.current["publication"])
        cls.publication_bytes = cls.publication_path.read_bytes()
        cls.publication = json.loads(cls.publication_bytes)

    def test_current_authority_pointer_matches_publication_bytes_and_identity(self) -> None:
        observed = "sha256:" + hashlib.sha256(self.publication_bytes).hexdigest()
        self.assertEqual(self.current["schemaVersion"], 1)
        self.assertEqual(self.current["kind"], "ordivon.research-owner-current")
        self.assertEqual(self.current["ownerResearchRef"], OWNER)
        self.assertEqual(self.current["authorityRef"], AUTHORITY)
        self.assertEqual(self.current["currentAuthorityVersionRef"], observed)
        self.assertEqual(self.publication_path.stem, observed.removeprefix("sha256:"))
        self.assertEqual(self.publication["ownerResearchRef"], OWNER)
        self.assertEqual(self.publication["authorityRef"], AUTHORITY)

    def test_current_publication_source_and_recovery_are_recoverable(self) -> None:
        source = self.publication["source"]
        self.assertEqual(source["kind"], "git")
        revision = source["sourceRevision"]
        self.assertRegex(revision, r"^[0-9a-f]{40}$")
        if (ROOT / ".git").exists():
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", revision, "HEAD"],
                cwd=ROOT,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        recovery = self.publication["currentRecovery"]
        self.assertEqual(recovery["targetRole"], "OWNER_RESEARCH_CORPUS")
        _relative_file(recovery["locator"])

    def test_all_declared_closeout_provenance_is_owner_native_recoverable(self) -> None:
        closeouts = self.publication["closeouts"]
        self.assertEqual(len(closeouts), 6)
        count = 0
        for closeout in closeouts:
            provenance = closeout["provenance"]
            self.assertTrue(provenance)
            for locator in provenance:
                _relative_file(locator)
                count += 1
        self.assertEqual(count, 24)

    def test_current_formal_core_and_executable_boundary_are_declared(self) -> None:
        corpus = json.dumps(self.publication, ensure_ascii=False)
        for token, locator in {
            "formal-core-reference-contract-v1": "FORMAL-CORE-REFERENCE-CONTRACT.md",
            "conformance-witness-v1": "conformance-witness/README.md",
            "phase-ii-project-constitution": "PHASE-II-PROJECT-CONSTITUTION.md",
        }.items():
            self.assertIn(token, corpus)
            _relative_file(locator)
        boundary = (ROOT / "EXECUTABLE-BOUNDARY.md").read_text(encoding="utf-8")
        self.assertIn("Disposable Conformance Witness ADMITTED", boundary)
        self.assertIn("Production Service NOT ADMITTED", boundary)


if __name__ == "__main__":
    unittest.main()
