# UCNS Boundary

**Status:** Boundary discipline doc. Pins name and proof-scope distinctions
across the four repos that touch UCNS-shaped artifacts.
**Date pinned:** 2026-05-22
**Companion docs:**
- `docs/handoffs/2026-05-22-ucns-g-prime-cylinder-v3.md` (UCNS-G v3 pin)
- `The-Interdependency/ucns:docs/ucns-shape-reconciliation.md` (PARALLEL verdict)
- `The-Interdependency/ucns:docs/ucns-g-prime-cylinder-supplement.md` (UCNS-G v3 supplement)

## 1. Vocabulary

These are not synonyms. They are distinct objects in distinct repos.

| Name | Repo | What it is |
|------|------|------------|
| **UCNS-A** | `The-Interdependency/ucns` | Recursive factorization algebra — `UCNSObject(n_dec, n_min, A_plus, F_plus)` with `(angle, payload)` anchors, modulo-4 doubled-cover angle arithmetic, payload recursion, face bits, XOR face composition. |
| **UCNS-G** | EDCM metric geometry (pinned by edcmbone) | Prime-indexed tensor of non-closing Möbius-cylinder metric disks. See `docs/handoffs/2026-05-22-ucns-g-prime-cylinder-v3.md`. |
| **`edcmbone.ucns` (local)** | this repo | Local **closed-token / marker encoding layer**: `closed_tokens.py` and `core/behavioral/ucns_marker_store.py`. Maps closed-class tokens and behavioral markers to UCNS-shaped record types for measurement purposes. |
| **`edcmbone` overall** | this repo | Structural transcript measurement package. Computes the scalar EDCM metric vector M_t (C, R, F, E, D, N, I, O, L, P, κ) plus PCNA/PCTA-style telemetry. |

## 2. Proof boundary

**Theorem N (in `The-Interdependency/ucns`) does not validate edcmbone or
EDCM metric claims.**

The factorization-algebra proofs in the `ucns` repo are scoped to UCNS-A.
They say nothing about:

- the scalar EDCM metric vector in
  `Backend/src/edcmbone/metrics/compute.py` /
  `backend/src/edcmbone/metrics/compute.py`,
- the behavioral-metric pipeline in
  `core/behavioral/behavioral_metrics.py`,
- the UCNS-G v3 metric-disk schema in `edcmbone/ucns_g/`,
- the local closed-token UCNS encoder in `closed_tokens.py`,
- any audit telemetry emitted under `raw_counts.ucns_hits_by_metric`.

The PARALLEL verdict from
`The-Interdependency/ucns:docs/ucns-shape-reconciliation.md` stands
unless an explicit bridge is constructed and tested (see
`The-Interdependency/ucns:docs/edcm-edcmbone-bridge-checklist.md`).

## 3. What `edcmbone.ucns` is and is not

`edcmbone`'s local UCNS surface is a **measurement / encoding layer**.

It is:

- **closed-class token encoding** — `closed_tokens.py` encodes a fixed
  vocabulary of grammatical tokens into UCNS-shaped record types on a
  16-gonal host carrier so transcripts can be projected into a stable
  symbolic basis.
- **behavioral marker hits** — `core/behavioral/ucns_marker_store.py`
  builds a marker-phrase store; `core/behavioral/behavioral_metrics.py`
  optionally records hit counts per behavioral metric under
  `raw_counts.ucns_hits_by_metric`.

It is **not**:

- a re-implementation of UCNS-A's recursive factorization algebra,
- a proof carrier for UCNS-A theorems,
- a canonical implementation of UCNS-G v3 geometry (the schema in
  `edcmbone/ucns_g/` is the v3 schema; the wider geometry remains open
  per the v3 handoff §13).

The local encoder reuses the UCNS shape vocabulary for convenience and
audit; it does not import proof status.

## 4. Telemetry status

UCNS-shaped output from `edcmbone` is **audit telemetry**, not a scored
metric, unless and until a later spec/test explicitly promotes it.

Concretely:

- `raw_counts.ucns_hits_by_metric` (when present) is **experimental
  audit telemetry**. The current behavioral metric formulas
  (`C, R, D, N, L, O, F, E, I`) in
  `core/behavioral/behavioral_metrics.py` do **not** consume
  `ucns_hits_by_metric` to alter their values.
- The local closed-token encoder's output (UCNSObject records produced
  by `closed_tokens.encode`) is a symbolic projection of token shape,
  not a proof token.
- The v3 schema in `edcmbone/ucns_g/` is a **schema-only** carrier; no
  scoring runtime currently consumes it.

If a future change promotes UCNS telemetry into a scored input, that
change must (a) update this doc, (b) add tests pinning the new
contribution, and (c) cite the source-backed bridge from the
`The-Interdependency/ucns:docs/edcm-edcmbone-bridge-checklist.md`.

## 5. Cross-repo non-transfer rule

For every repo in the ecosystem, the rule is:

```text
UCNS-A theorem/proof status does NOT transfer to:
  - UCNS-G metric geometry
  - EDCM metric vector outputs
  - edcmbone behavioral metric outputs
  - edcmbone.ucns local encoding outputs
  - a0 EDCM runtime outputs
  - any interdependent-lib aggregate
unless an explicit, source-backed bridge with reverse-recoverability
limits and tests has been added under
The-Interdependency/ucns:docs/edcm-edcmbone-bridge-checklist.md.
```

PR descriptions that touch UCNS surfaces should state:

> No UCNS-A theorem/proof status is transferred to EDCM, edcmbone, or
> UCNS-G by this change.

## 6. Open items (carried from v3 §13)

- Formal exchange rules between typed units `1_R`, `1_C`, `1_A`, `1_Z`.
- Exact prime assignment for any composite / coupling positions beyond
  the 14 primitive axes in `edcmbone/ucns_g/primes.py`.
- DRIFT / DVG / DA mapping into the prime-cylinder graph.
- Whether UCNS-A can provide a formal bridge to UCNS-G structure
  (currently no; see PARALLEL verdict).
- Schema vs code migration order for replacing scalar EDCM outputs with
  v3 metric-disk tensors (currently: scalar stays as projection, schema
  is additive).
