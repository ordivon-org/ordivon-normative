# Ordivon Normative Formal Core Reference Contract v1

Status: **CURRENT / FROZEN IN SCOPE**.

This document consolidates the N0–N6 formal research and the N7–N11 falsification/dogfood results. It is technology-neutral semantic authority. It does not prescribe a storage model, programming language, proof calculus, database schema, API, service, or ontology implementation.

## 1. Owner boundary

Ordivon Normative owns context-relative constitutive/normative **admission, applicability, consequence, competence/power, and valid transformation semantics**.

It imports externally owned facts and domain content. It does not thereby own World facts, Human psychology, Game content, Finance content, Harness/Runtime execution, generic institutions/governance, legitimacy simpliciter, universal morality/Normativity, generic reasons/value/ought/fittingness, generic Control/Regulation, or generic Representation.

## 2. Minimal observable judgment kernel

The smallest currently supported observable interface has three relation families:

- `ExternalAt(F, K)` — an externally owned premise/reference supplied at context cut `K`.
- `Assessed_C(Sign, Phi, K)` — a signed context-relative assessment of typed claim `Phi`.
- `Supports_C(D, Bases, Sign, Phi, K)` — one identifiable semantic support/derivation path `D`.

`Context`, `ContextCut`, `Claim`, and `DerivationWitness` are formal interface categories, not numbered Foundations or ontic primitives.

### Signed standing

`affirm Phi` and `deny Phi` are independently supportable judgments.

- affirm only: positive standing;
- deny only: explicit negative/non-standing judgment appropriate to the typed claim;
- neither: unknown / unresolved / unassessed;
- both: explicit inconsistent assessment.

`deny Phi` is not automatically classical object-language negation. Absence of affirm never produces deny unless an admitted context rule supplies a denial path.

## 3. Support and standing

`SupportPath != StandingSufficiency`.

A support path may exist while remaining advisory, defeated, inapplicable, incomplete, or otherwise non-dispositive. An authoritative assessment requires at least one support path that is context-qualified as standing-sufficient at the supplied cut.

Standing sufficiency is path-local. Multiple independent paths may support the same claim; loss of one path does not erase another or rewrite support history.

No universal rule `Supports -> Assessed` is admitted.

## 4. Three intervention loci

The formal core must keep distinct:

1. **Source standing/effectivity** — whether the relevant generator/source is admitted/effective.
2. **Applicability/qualification** — whether that source applies to the case/query.
3. **Path standing-sufficiency** — whether one concrete support path is dispositive at the cut.

A source repeal is not merely downstream defeat. An applicability exception is not source invalidity. A path blocker need not alter either source standing or applicability.

## 5. Conflict and defeat

`Conflict != Invalidity != Defeat != Deletion`.

Incompatible standing claims may coexist when no admitted resolution rule defeats either path. Conflict alone does not cancel standing.

At the current owner-general level, defeat proper requires only path-local disqualification from standing sufficiency. Priority override, undercutting, procedural bars, and some exceptions may have distinct typed explanations while sharing that general effect. Richer PHR4 defeat distinctions remain preserved research interfaces but are not promoted into the minimal owner core without a forcing counterexample.

Blocking an affirm path does not create deny.

## 6. Temporal standing and effect lifecycle

Mandatory separations:

- `Admission != Effectivity`;
- `Suspension != Termination`;
- `SourceEffectivity != CreatedEffectCurrentness`;
- `HistoricalStanding != CurrentStandingAtCut`;
- `EvaluationCut != Target/ReferenceTime`;
- `RetroactiveEffect != HistoryRewrite`;
- `NormativeLineage != ChronologicalLaterness`;
- `Reinstatement != NewIdentity`.

Wall-clock/time facts are external premises. They acquire normative consequence only through admitted temporal semantics.

No interval/phase ontology is required: cut-indexed signed claims plus typed temporal/lineage/change claims currently suffice. Interval representations remain optional.

Current authoritative cut selection is outside the minimal semantic kernel. The caller/owner-currentness surface supplies the cut; Normative evaluates at that cut.

## 7. Normative power and valid change

Minimal competence form:

`Power_C(Subject, Delta)`

where `Delta` is a typed normative change description.

`Permission != Power != Capability != EffectiveControl`.

Power possession is distinct from whether a concrete event validly realizes the change. `ValidChange(K_pre, Event, Delta)` is predecessor/lineage-relative.

Delegation, revocation, subdelegation, succession, transfer, amendment, ratification, genesis, and replacement are typed normative changes. Possessing `Power(S, Delta)` does not imply `Power(S, GrantPower(...Delta...))`, revocation power, or transfer power.

A valid delegation creates a new support path for the recipient's Power claim. Authority provenance may have multiple independent sources and is therefore generally graph-capable rather than universally tree-shaped.

Technical/process/model/memory/credential continuity does not itself create normative succession or transfer.

## 8. Multi-context semantics

Contexts are independent by default.

`Assessed_C1(Phi)` has no normative force in `C2` merely because the surface claim/action/entity is shared.

Cross-context influence requires a standing-sufficient support path owned by the receiving or an admitted bridge context. A source-context assessment may be a provenance-preserving dependency, but it does not self-import.

Translation may requalify type, scope, sign, temporal standing, or consequence. Therefore `CrossContextInfluence != PropositionTokenIdentity`.

Jurisdiction/Governs/Recognizes/Translates are typed claim roles expressible through the same kernel. No universal context merge, type-based priority, or global `is_allowed()` answer is admitted.

## 9. History, provenance, and operational boundary

Artifact identity, authenticity/provenance, source standing, support, normative assessment, operational execution, and semantic success remain distinct truth roles.

Storage does not mint authority. Runtime/Harness/Game execution success does not establish normative validity. Operational denial does not by itself establish normative prohibition.

Historical assessments and support paths remain queryable after supersession, defeat, withdrawal, revocation, reclassification, or later retroactive effects.

## 10. Representation plurality

Three materially different representation families survived the frozen N0 corpus:

- generator/history-primary;
- proposition/state-primary;
- transition/judgment-history-primary.

Therefore representation primacy is **UNDERDETERMINED** by current semantic evidence. Formal convenience cannot establish semantic or ontic primitiveness.

Likewise, explicit interval objects, detailed defeat taxonomies, structured competence records, authority trees/graphs, and context graphs are optional representations unless future counterexamples force them.

## 11. Reopen rule

Reopen this formal core only when a concrete counterexample or dogfood case:

- cannot be represented without violating a core separation; or
- demonstrates that a current core obligation is unnecessarily strong.

New domain nouns, implementation convenience, API ergonomics, storage pressure, or downstream importance alone do not reopen the semantic core or admit a numbered Foundation.
