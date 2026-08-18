# Non-canonical Fixture Interchange v1

> This document describes a disposable test encoding. It is **not** an Ordivon Normative schema, ontology, API, or storage contract.

Each fixture contains one or more explicit evaluations. An evaluation names a `context` and `cut`, a set of typed test premises, support paths, and expected observations.

A support path has:

- an opaque `id`;
- signed target claim: `affirm` or `deny`;
- opaque claim text;
- explicit base references;
- explicit `standingSufficient: true|false`;
- optional premise IDs in `blockedBy`.

Base references are either:

- `{"premise": "<id>"}` — an explicit supplied premise; or
- `{"assessment": {"sign": "...", "claim": "..."}}` — a signed assessment derived by another standing path in the same evaluation.

The evaluator performs one monotone fixpoint only. A path yields its signed assessment iff all bases are satisfied, the path is explicitly standing-sufficient, and none of its explicit blockers is active.

No other inference exists. In particular:

- missing `affirm P` does not produce `deny P`;
- blocking `affirm P` does not produce `deny P`;
- two different paths may support the same claim;
- `affirm P` and `deny P` may coexist;
- a `cross-assessment` premise remains a provenance-bearing supplied dependency; the witness does not auto-import it into the receiving context.

The JSON shape may be replaced at any time. Only conformance to the frozen semantic contract and regression behavior matters.
