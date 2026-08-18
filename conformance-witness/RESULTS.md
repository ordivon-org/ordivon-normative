# Conformance Witness Result — N11 Initial Backend

> **NON-AUTHORITATIVE EXECUTION EVIDENCE**

Baseline shared-repository revision: `edfb2bb80803a586636804015169f0c01d6e9709`.

Normative semantic AuthorityVersionRef before implementation: `sha256:6558bc84bb52a3a0ffbff0f683a36d46c28efc0f2ba531d4458bd5aa16a4a56e`.

## Executable regression

`python3 run_regression.py`

- fixture count: **66**
- passed: **66**
- failed: **0**
- NCX: 16/16
- NCF: 6/6
- N3F: 8/8
- N4F: 7/7
- N5F: 9/9
- N6F: 7/7
- GDF: 8/8
- HAG (actual Harness/Agent executable boundary checks): 5/5

Runtime execution evidence: `job-01a015a9-278d-7de2-9598-f207e4379f57`.

## Implementation invariant tests

`python3 -m unittest -v test_witness.py`

- tests: **7**
- passed: **7**
- failed: **0**

The tests cover fail-closed missing-cut behavior, neither/both signed states, support-only non-standing, blocked-path non-sign-flip, and multi-step assessment dependency.

Runtime execution evidence: `job-01a015a9-4b36-7b31-b4ba-e8077d8bf2fb`.

## Interpretation boundary

A green result means only that this disposable backend reproduces the explicitly encoded thin-calculus fixtures. It does **not** establish the truth of a domain rule, select an authoritative current cut, authorize an action, or promote this JSON/Python representation to Normative ontology.

Any future discrepancy between this code and the frozen semantic contract is evidence against the code first, not automatic evidence against the semantic owner.
