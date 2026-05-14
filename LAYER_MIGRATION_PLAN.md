# LAYER_MIGRATION_PLAN.md — edcmbone → `edcm` upstream package

**Date:** 2026-05-14
**Branch:** `claude/audit-regrade-four-layer-uiveg`
**Companion doc:** `AUDIT_REGRADE.md` (re-graded findings).

hmmm: this document represents grading against held canon as of 2026-05-14; canon may evolve. The future `edcm` package is **not yet named, not yet existing, and not yet located** — every reference to `edcm/...` paths below is a placeholder shape.

hmmm: no files are moved by this document. No package is created. No Python code is modified. This is a contract, not an execution.

---

## Held canon (recap)

- **L0** — bones-only operator layer. Closed-class tokens, P/K/Q/T/S families, operator vector O ∈ ℝ⁵. **edcmbone is canonical L0 only.**
- **L1** — Arc Style. `M_t = A·φ` where φ = L0 primitives, A = canonical weight matrix.
- **L2** — risk composites built atop L1 outputs.
- **L3** — projection. 6 agent-facing metrics: CM, DA, DRIFT, DVG, INT, TBF.
- **Bridge** — sideways, observational-only correlation between Operator (L0) and Behavioral concerns. Orthogonal to the layer stack.
- The **9 Behavioral metrics** (C R D N L O F E I) are a slice across L1/L2; not a layer.

The future upstream package `edcm` consumes edcmbone (L0) and `ucns` (UCNS encoder) and produces L1/L2/L3.

---

## Section A — files canonically L0 (stay in edcmbone)

These remain in edcmbone after migration. Within edcmbone, parallel implementations are consolidated to a single canonical version (Phase 1).

- `closed_tokens.py` (repo root) — L0 closed-class token table.
- `Backend/src/edcmbone/ucns/` — UCNS encoder. Stays here only if `ucns_v04.py` is canon-pinned as L0; otherwise migrates to `ucns`. (See `hmmm` below.)
- `ucns_v04.py` (repo root) — same `hmmm`.
- **One of** `Backend/src/edcmbone/parser/turns_rounds.py` **or** `core/parsing/{tokenizer,normalizer,turn_builder,round_builder}.py` — whichever wins Phase 1 consolidation. The losing side is retired.
- `Backend/src/edcmbone/canon/loader.py` and `Backend/src/edcmbone/canon/data/*.json` — L0 canon data.
- `Backend/src/edcmbone/metrics/stats.py` — TTR, entropy, cosine, n-grams. These are **L0 sub-primitives** (counting / distributional functions over raw tokens), not L1 Arc Style metrics. They stay.
- `Backend/src/edcmbone/compress.py` — lossless codec for L0 data structures.
- `core/operator/` (matcher, operator_extractor, etc.) — operator-layer construction from L0 tokens. Stays as L0.

hmmm: `metrics/stats.py` is grouped here under "L0 sub-primitives," but TTR / entropy / cosine are not bones; they are distributional measurements **over** L0 tokens. Whether canon classifies them as L0 (because they are pre-Arc-Style primitives) or as L1 base inputs (because they feed `M_t = A·φ`) is unresolved. Re-classify before migration if canon pins this.

hmmm: if `ucns_v04` migrates to `ucns`, all of `Backend/src/edcmbone/ucns/` follows it. Then edcmbone's L0 surface shrinks to closed_tokens + canon + parser + compress + operator.

---

## Section B — files canonically L1 (migrate to `edcm/arc_style/` or equivalent)

- `Backend/src/edcmbone/metrics/matrix.py` — `A_MATRIX` plus the doc-statement that `M_t = A·φ`. This is the canonical L1 contract.
- The portion of `Backend/src/edcmbone/metrics/compute.py` that computes Arc Style metrics. This is **not the entire file** — `compute.py` orchestrates L1/L2/L3 (see §F). The L1 portion needs surgical extraction.
- The L1-side helpers currently in `core/behavioral/behavioral_metrics.py` — per-window L1-style computations (the cosine-vs-previous-window code path and similar). (See §F for the split rationale.)

hmmm: Finding 07 (`A_MATRIX` declared but not consumed) and Finding 08 (`A_MATRIX["E"]` references an L1 metric) both must be resolved **before** the matrix migrates. Migrating a load-bearing-but-disconnected contract amplifies the defect.

hmmm: the held canon does not enumerate the 11 Arc Style metrics by letter. Migration cannot safely extract "the L1 portion of compute.py" until a canonical metric-to-layer table exists. Without it, the L1/L2 split inside `compute.py` is a judgement call per metric.

---

## Section C — files canonically L2 (migrate to `edcm/risk/`)

- `Backend/src/edcmbone/metrics/risk.py` — the four risk-proxy functions.
- The portion of `compute.py` that assembles risk composites from L1 outputs.
- The L2-side helpers currently in `core/behavioral/behavioral_metrics.py` — per-window composite computations (fixation, rep-ngram-novelty stacks, etc.).

hmmm: Finding 29 (`broken_return` not clamped) and the F-double-definition (Finding 05) both intersect this section. Pin canonical operationalizations before migrating.

---

## Section D — files canonically L3 (migrate to `edcm/projection/`)

- `Backend/src/edcmbone/metrics/projection.py` — `AgentMetrics`, `PROJECTION_MAP`, `fire_alerts`, `project_transcript`.
- The portion of `compute.py` and any caller that constructs the agent-facing 6-tuple (CM, DA, DRIFT, DVG, INT, TBF).

hmmm: Finding 30 (`fire_alerts` only handles `direction="above"`) intersects this section. If canonical L3 requires bidirectional alerts, resolve before migration.

hmmm: TBF lives at L3 per canon (it is in the 6-tuple), but the `gini_tbf` implementation may currently sit alongside L2 risk code. Surgical extraction needed.

---

## Section E — files sideways (Bridge — observational correlation)

Bridge sits orthogonal to L0/L1/L2/L3. It correlates Operator (L0) outputs against Behavioral (slice) outputs without modifying either. Files:

- `core/bridge/bridge_engine.py`
- `core/bridge/math_utils.py`
- any caller / configuration glue specific to Bridge.

These do **not** migrate into `edcm/arc_style/`, `edcm/risk/`, or `edcm/projection/`. They live wherever the Bridge package canonically lives.

hmmm: Bridge's physical home is unresolved — candidates include edcmbone (kept as a sideways co-resident), the future `edcm` package (as a sub-namespace), or a separate `interdependent-lib` / similar. The decision affects (a) which package owns the Welford-fix from Finding 23, (b) which package's tests pin Bridge's read-only correlation contract.

hmmm: Bridge's read-only contract requires that the L0 stream it consumes be deterministic across consumers. Findings 12, 13, and 14 (parser drift) directly threaten this contract. Bridge migration cannot precede parser consolidation.

---

## Section F — files of uncertain home (per-file decision needed)

These cross layer boundaries internally and require per-file disposition.

- **`core/behavioral/behavioral_metrics.py`** — the 9-metric Behavioral concern is a slice across L1/L2, not a layer. Recommended split:
  - Per-window L1-style computations (cosine-vs-previous-window etc.) → `edcm/arc_style/` (§B).
  - Per-window L2-style risk composites → `edcm/risk/` (§C).
  - Any Bridge-facing emission glue → stays sideways with Bridge (§E).
- **`Backend/src/edcmbone/metrics/compute.py`** — orchestrator across L1/L2/L3. Belongs in `edcm/` as the **top orchestrating module that consumes edcmbone L0 outputs and produces L1/L2/L3**. After migration, edcmbone has no `compute.py`; the orchestration lives upstream.
- **`engine.py` at repo root** — `analyze_transcript` orchestrator. Same disposition as `compute.py` — top-level `edcm` entry point.
- **`Backend/src/edcmbone/metrics/__init__.py`** — currently re-exports L0/L1/L2/L3 symbols. After migration, it re-exports only L0 sub-primitives (the `stats.py` surface); the L1/L2/L3 re-exports move to `edcm/__init__.py`.
- **`Tests/test_backend.py` (87-test suite)** — split per layer. L0 tests stay in edcmbone; L1/L2/L3 tests move with their respective code into the new `edcm` package. The split must preserve the existing pass-rate invariant before any code migration is considered done.

hmmm: `compute.py` and `engine.py` are both "the orchestrator" at different scales. Whether `edcm` exposes both or unifies them under a single entry point is unresolved.

hmmm: the L0/L1/L2/L3 split of the 87-test suite has not been audited. Some tests may exercise multiple layers in a single assertion (especially round-trip tests); those need test-level disentanglement before migration, not just relocation.

hmmm: `P` (Finding 06) is referenced from `compute.py` but absent from the 9-metric Behavioral list. Until canon places `P` at L1, L2, or "drop," its `compute.py` block cannot be assigned a destination subdirectory.

---

## Sequencing recommendation

### Phase 0 — implementation bugs that are canon-independent

**Goal:** make edcmbone shippable as a package before any migration begins. Migration into a non-installable, case-colliding package compounds risk.

Scope:
- Finding 01 — collapse case-collision directory pairs.
- Finding 02 — fix bare top-level import; make `pip install ./backend` produce a working `import edcmbone` surface.
- Finding 03 — fix normalizer no-op replace.
- Finding 04 — byte-level verify parser apostrophe regex; fix if drift exists.
- Finding 15 — rename all `hmm` → `hmmm` across the five identified files.
- Finding 19 — byte-level verify `WHITESPACE_TABLE` for ASCII-space ↔ NBSP collision.

No file moves. No layer code touched. No `edcm` package created.

Exit criteria: `pip install ./backend && python -c "import edcmbone; import edcmbone.ucns; import edcmbone.parser; import edcmbone.metrics; import edcmbone.compress"` succeeds from a non-repo cwd, and the 87-test suite passes from an installed location.

hmmm: Phase 0 is conditional on Erin's resolution of "canonical directory casing per pair" (Finding 01) and "is `ucns_v04.py` an L0 file or upstream" (Finding 02). Both are canon-shaped questions blocking implementation work.

### Phase 1 — parallel-parser consolidation

**Goal:** one canonical L0 parser, one drift-control contract.

Scope:
- Pick the canonical parser (Backend production or core refactor side).
- Add Finding 38's cross-pipeline convergence test as the retiring side's death-regression net.
- Resolve Findings 12, 13 (SYS/TOOL anchoring, contraction tokenization) per the winning parser's canon decision.
- Retire the other side: deletion or archive.
- Update the convergence test to single-side, or drop it.

Exit criteria: one parser in the tree; the 87-test suite (now extended with the post-consolidation tests) passes; Findings 12, 13, 14 are closed.

hmmm: which parser wins consolidation is unresolved. Refactor side has architectural separation; Backend side has the 87-test suite. The decision is canon-adjacent, not purely engineering — see `hmmm` in `AUDIT_REGRADE.md` Finding 14.

### Phase 2 — create the `edcm` package; migrate L1 (Section B)

**Goal:** stand up the upstream package and move the Arc Style layer into it.

Scope:
- Create `edcm` package at its canonical location.
- Migrate `metrics/matrix.py` and the L1 portion of `compute.py` to `edcm/arc_style/`.
- Migrate the L1-side helpers from `core/behavioral/behavioral_metrics.py`.
- Wire the migrated `compute_arc_style` (or equivalent) through `A_MATRIX` (resolves Finding 07).
- Fix `A_MATRIX["E"]` layer-mix (resolves Finding 08) before wiring.
- Update edcmbone tests to no longer exercise L1 code.
- Add tests in `edcm/arc_style/` for the migrated files.

Exit criteria: edcmbone has no L1 code; `edcm/arc_style/` runs L1 computation against edcmbone-L0 outputs; tests pass on both sides.

hmmm: the location of the `edcm` package — new repo, sub-directory of an existing repo, monorepo workspace — is unresolved. The decision affects PyPI release plan, dependency direction, and contributor onboarding.

hmmm: held canon does not enumerate the 11 Arc Style metrics. The L1 portion of `compute.py` cannot be precisely extracted without that enumeration. Phase 2 is gated on canon pinning the metric-to-layer table.

### Phase 3 — migrate L2 (Section C)

Scope:
- Migrate `metrics/risk.py` and the L2 portion of `compute.py` to `edcm/risk/`.
- Migrate L2-side helpers from `core/behavioral/`.
- Resolve Findings 29 (clamp consistency) and 05 (F double-definition) at migration boundary.

Exit criteria: edcmbone has no L2 code; `edcm/risk/` consumes L1 outputs from `edcm/arc_style/`.

### Phase 4 — migrate L3 (Section D)

Scope:
- Migrate `metrics/projection.py` (AgentMetrics, PROJECTION_MAP, fire_alerts, project_transcript) to `edcm/projection/`.
- Resolve Finding 30 (bidirectional alerts) at migration boundary.

Exit criteria: edcmbone has no L3 code; `edcm/projection/` consumes L2 outputs.

### Phase 5 — migrate Section F per-file (and dispose Bridge)

Scope:
- Per-file split of `core/behavioral/behavioral_metrics.py` between `edcm/arc_style/` and `edcm/risk/`.
- Migrate `compute.py` (orchestrator residue) and `engine.py` to `edcm/`.
- Split `Tests/test_backend.py` along L0 / L1 / L2 / L3 axes; relocate the upper-layer tests.
- Resolve `P` (Finding 06) into its canonical layer or drop.
- **Bridge disposition (parallel sub-track):** decide Bridge's physical home (edcmbone sideways / `edcm` sub-namespace / separate lib); apply Finding 23 (Welford O(n) fix) in the canonical home; pin Bridge's read-only correlation contract via tests against the post-consolidation L0 stream and the post-migration L1/L2 streams.

Exit criteria: edcmbone is L0-only; every layer-mixing orchestrator file is gone from edcmbone; Bridge has a single canonical home with its correlation contract tested.

hmmm: the Bridge sub-track has no strict ordering with the rest of Phase 5 — it depends on the home-decision, not on whether `compute.py` has migrated. Could run in parallel.

### Phase 6 — cleanup pass

Scope:
- Findings 17, 18, 21, 22, 24, 25, 26, 27, 28 — dead code, unused imports, stale docstrings, named constants, JSON caching, hardcoded section lists, type fixes.
- Done **after** each file's migration so cleanup doesn't conflict with relocation diffs.

Exit criteria: all S3/S4 cleanup findings closed.

### Phase 7 — test coverage backfill

Scope:
- Findings 32–37, 39 — round-trip, affix false-positive, monologue, SYS/TOOL exclusion (post-consolidation), smart-apostrophe, normalizer, refactor-pipeline per-component tests (if refactor side won Phase 1).

Exit criteria: all test-gap findings closed; coverage measured against migrated package surface.

---

## Critical `hmmm`s in the migration plan

- **hmmm:** Location of the future `edcm` package — new repo, sub-directory of an existing repo, monorepo workspace. Affects PyPI release plan and import direction.
- **hmmm:** Whether L1/L2/L3 migration happens before or after edcmbone's case-collision and not-installable Phase 0 fixes. This plan recommends Phase 0 first; deviating compounds risk.
- **hmmm:** The 11 Arc Style metrics (L1) and the 9 Behavioral metrics list (C R D N L O F E I) overlap but aren't identical. Pin which letters are L1 Arc Style and which are L2 composites before Phase 2 begins.
- **hmmm:** `P` metric (Finding 06) — which layer does it belong to once L1/L2/L3 are separated? Currently in `compute.py`. Cannot be Phase-5-migrated without a layer assignment.
- **hmmm:** Bridge layer's physical home — edcmbone sideways, `edcm` sub-namespace, or a third package. Best fit pending.
- **hmmm:** Whether `ucns_v04.py` is canonical L0 (stays in edcmbone) or migrates to `ucns` upstream. Affects edcmbone's L0 surface area.
- **hmmm:** Which parser wins Phase 1 consolidation. Architectural separation (refactor) vs. test coverage (Backend).
- **hmmm:** Whether `metrics/stats.py` is L0 sub-primitives (stay) or L1 base inputs (migrate). Canon does not pin this.
- **hmmm:** Whether `edcm` exposes both `compute.py` and `engine.py` as orchestrators or unifies them.

---

## What this document does **not** do

- Does not move any files.
- Does not create the `edcm` package.
- Does not modify any Python code.
- Does not file any GitHub issues.
- Does not enumerate the 11 Arc Style metrics or the L2 composite names — held canon does not pin them; per the brief's "do not enumerate" rule, every metric-to-layer judgement above is grounded in file location and the `M_t = A·φ` contract, not in a canonical letter-to-layer table.
- Does not auto-resolve any `hmmm`. Resolution awaits Erin.

hmmm: end of document.
