# Normative Conformance Witness

> **NON-AUTHORITATIVE · NON-CANONICAL · NON-PRODUCTION · DISPOSABLE**

This directory is executable falsification infrastructure for the frozen **Ordivon Normative Formal Core Reference Contract v1**. It is not the Normative semantic authority, not a rule/policy engine, not a production authorization service, and not a canonical data schema.

Semantic authority remains the owner-native publication under `../authority/` and its upstream research contract. This witness must remain replaceable without changing owner truth.

## What it does

The witness accepts an explicit fixture at a caller-supplied context/cut and executes only the admitted thin calculus:

`explicit premises + Supports path + explicit standing-sufficiency + no explicit blocker -> signed Assessed claim`

It preserves:

- `affirm` / `deny` / neither / both;
- `Supports != StandingSufficiency`;
- path-local blocking without deletion or sign flipping;
- multiple independent support paths;
- explicit assessment dependencies for multi-step derivations;
- cut/context labels and cross-context provenance as opaque fixture premises.

Every assessment produced by the witness has a trace to one standing support path.

## What it deliberately does not do

It does **not**:

- discover or resolve the authoritative current cut;
- parse prose, compile domain rules, or invent support paths;
- infer denial from missing support;
- automatically merge contexts or copy authority across contexts;
- infer permission from capability, power from permission, or delegation power from object power;
- persist/admit/revoke normative truth;
- call Runtime/Harness/Game to enforce actions;
- expose `is_allowed() -> bool`;
- define a canonical Normative ontology or serialization.

`fixtures.json` is explicitly a **non-canonical interchange encoding**. Opaque claim strings are test tokens only.

## Run

```bash
python3 run_regression.py
python3 -m unittest -v test_witness.py
python3 witness.py fixtures.json --fixture NCX-014
```

A regression failure is evidence to investigate. Implementation output never outranks the frozen semantic contract or fixture meaning.
