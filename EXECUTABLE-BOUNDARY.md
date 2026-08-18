# Executable Boundary

Current decision: **Disposable Conformance Witness ADMITTED; General Kernel / Production Service NOT ADMITTED**.

## Admitted executable role

The owner permits a replaceable research/conformance witness whose purpose is:

- deterministic replay of explicit frozen fixtures;
- regression detection;
- inspection of signed assessments and support traces;
- falsification of accidental semantic collapse.

The current witness is one implementation witness only. It is not semantic authority.

## Mandatory boundaries

An admitted witness:

- receives an explicit context and evaluation cut;
- consumes explicit external premises, typed claims, support paths, standing-sufficiency/blocker qualifications, lineage/temporal references, and explicit cross-context references;
- preserves affirm / deny / neither / both;
- emits derivation traces and failed/missing bases;
- fails closed rather than guessing an authoritative current cut or missing domain semantics;
- remains disposable and reimplementable.

It must not:

- write/admit/revoke persistent normative truth;
- resolve `current` owner authority/cut;
- parse prose or invent a domain rule language;
- infer domain support paths not supplied by the fixture/context adapter;
- automatically merge contexts or copy authority across them;
- infer deny from absence;
- perform Runtime/Harness/Game execution or enforcement;
- expose a production `is_allowed() -> bool` authority surface;
- become a required dependency for domain correctness.

## Rejected executable roles

Current evidence does **not** admit:

- a universal normative rule/policy DSL;
- a general-purpose normative inference kernel;
- a persistent normative truth database;
- a production Normative API/MCP/service;
- current-cut/current-authority resolution inside the evaluator;
- operational authorization/enforcement authority.

These remain separate future admission questions. Deployment momentum or implementation convenience cannot promote the conformance witness into any rejected role.

## Authority separation proven in N11

The witness was committed and pushed as owner-local non-semantic tooling while the owner `authority/` subtree remained byte-identical and the existing AuthorityVersionRef did not change. Therefore repository/source transport advancement does not mint semantic authority.
