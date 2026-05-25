# AUDIT_REGRADE.md — edcmbone audit re-graded against four-layer EDCM canon

**Date:** 2026-05-14
**Branch:** `claude/audit-regrade-four-layer-uiveg`
**Replaces / amends:** prior Claude.ai audit-session summaries.

hmmm: this document represents grading against held canon as of 2026-05-14; canon may evolve, and any subsequent canon change re-opens every grading decision below.

---

## Held canon used for re-grading

- **L0** — primitives. Bones-only operator layer: closed-class tokens, P/K/Q/T/S families, operator vector O ∈ ℝ⁵. **edcmbone is canonical L0 only.**
- **L1** — Arc Style. Metrics produced by the linear map `M_t = A·φ` where φ is the L0 primitives and A is the canonical weight matrix.
- **L2** — risk composites. Composites built atop L1 outputs.
- **L3** — projection. 6 agent-facing metrics (CM, DA, DRIFT, DVG, INT, TBF) projected from upper-layer state.
- **Bridge** — sideways observational-only correlation between Operator (L0) and Behavioral concerns. Not L4. Orthogonal to the layer stack.
- **Behavioral 9-metric slice (C R D N L O F E I)** — a slice across L1/L2 territory, not a layer.
- **hmmm enforcement** — every artifact must contain `hmmm`. Absence is fail-closed.

**Misplacement rule:** any L1/L2/L3 code currently inside edcmbone is **layer-misplaced**, not just internally drifting. Severity may rise on that basis.

hmmm: the held canon does not yet name the future upstream package that consumes edcmbone + `ucns`. This re-grading writes against an unnamed `edcm` placeholder.

---

## Per-finding re-grading

### Finding 01 — Case-collision dirs

**Original severity (audit session):** S1
**Re-graded severity against canon:** S1
**Canonical home:** canon-independent
**File(s):** `Backend/`, `backend/`, `Tests/`, `tests/`, `Frontend/`, `frontend/`
**Description:** Three pairs of directories differ only by case. Concrete evidence: `Tests/test_backend.py` is 23K real code; `tests/test_backend.py` is 0 bytes. On macOS HFS+/APFS and Windows NTFS, clone order determines which file survives — risk of silently losing the entire 87-test suite on contributor checkouts.
**Why severity changed (if it did):** unchanged; this is a filesystem-level repo bug, not a canon question.
**Remediation pattern:** in-place fix — collapse each pair into a single canonical-case directory before any layer migration begins.
**hmmm:** unresolved — which casing is canonical for each pair (`Backend` vs `backend`, etc.). The decision interacts with PyPI distribution and downstream imports.

### Finding 02 — Backend not installable as a package

**Original severity (audit session):** S1
**Re-graded severity against canon:** S1
**Canonical home:** canon-independent
**File(s):** `backend/src/edcmbone/ucns/closed_tokens.py` (bare `from ucns_v04 import …`)
**Description:** Bare top-level import to a module sitting at repo root. Works only when running with cwd at repo root. `pip install ./backend` followed by `import edcmbone.ucns` fails with `ModuleNotFoundError`. The "87 tests passing" claim is conditional on cwd, not on installed-package state.
**Why severity changed (if it did):** unchanged. The misplacement rule does not apply — this is about importability of L0 code that legitimately lives in edcmbone.
**Remediation pattern:** in-place fix — move `ucns_v04.py` and `closed_tokens.py` into the package proper, or rewrite imports to be package-relative.
**hmmm:** unresolved — whether the canonical home of `ucns_v04.py` is inside edcmbone at all, or whether it migrates to `ucns` (the other upstream consumer named in held canon).

### Finding 03 — Normalizer no-op

**Original severity (audit session):** S1
**Re-graded severity against canon:** S1
**Canonical home:** L0 (normalization is sub-primitive)
**File(s):** `core/parsing/normalizer.py::normalize_text_for_matching`
**Description:** `.replace("'", "'")` appears to map U+2019 → U+2019 (no-op). A second `.replace("'", "'")` (U+2018 → U+2019) plausibly works but is unverified. ASCII apostrophe U+0027 is never normalized. Smart-quoted contractions miss bones-map lookups silently.
**Why severity changed (if it did):** unchanged. Canonical L0 territory; the bug is in-place.
**Remediation pattern:** in-place fix in edcmbone after parallel-parser consolidation (Finding 14). Add unit test (Finding 36/37).
**hmmm:** unresolved — byte-level verification of the second `.replace` pair (U+2018 → U+2019) has not been done from this session. Read the file in `od -c` before fixing.

### Finding 04 — Parser apostrophe regex unverified

**Original severity (audit session):** S1
**Re-graded severity against canon:** S1
**Canonical home:** L0
**File(s):** `backend/src/edcmbone/parser/turns_rounds.py::_WORD_RE`, `backend/src/edcmbone/metrics/stats.py::_WORD_RE`
**Description:** Visually similar regexes between parser and stats. `stats.py` has a regression test (`test_tokenize_ascii_apostrophe_contraction`) asserting ASCII contractions stay whole. Parser has no equivalent. GitHub API rendering cannot distinguish U+0027 from U+2019 inside character classes.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** verify byte-level locally with `od -c` or hex viewer; if drift exists, fix in-place in edcmbone L0 parser; add parser-level regression test.
**hmmm:** unresolved — byte-level verification pending. Severity could drop to S3 if the regexes are byte-identical.

### Finding 05 — F-metric double definition

**Original severity (audit session):** S2
**Re-graded severity against canon:** S1
**Canonical home:** crosses L1/L2 (Behavioral slice) and Bridge
**File(s):** `Backend/src/edcmbone/metrics/compute.py::_compute_F`, `core/behavioral/behavioral_metrics.py` (or equivalent)
**Description:** Same canonical letter `F` operationalized two different ways — `fixation_risk` (rep + ngram + non-novelty) in one place, cosine similarity to previous window's feature vector in the other. Bridge correlates operator and behavioral outputs including F-vs-F → incomparable quantities measured under one name.
**Why severity changed (if it did):** rose from S2 to S1 because (a) the code is **layer-misplaced** (`compute.py` blends L1/L2/L3 inside edcmbone), and (b) Bridge's read-only correlation contract is invalidated by inconsistent upstream streams. Two violations stack.
**Remediation pattern:** migrate to upstream `edcm` package + canon-pin a single operationalization of `F` per layer. If both meanings are needed they need distinct letters.
**hmmm:** unresolved — which operationalization of F is canonical for L1 Arc Style vs L2 risk composite. Cannot grade without that decision.

### Finding 06 — `P` in compute.py out of the 9-list

**Original severity (audit session):** S2
**Re-graded severity against canon:** S2
**Canonical home:** uncertain — L1 or L2; not present in held 9-metric Behavioral slice
**File(s):** `Backend/src/edcmbone/metrics/compute.py`
**Description:** Produces `P` (`0.6 * novelty + 0.4 * entropy_gain`) which is not in the Canon Freeze 9-list (C R D N L O F E I). Could be canon-divergent extra or could belong at a different layer.
**Why severity changed (if it did):** unchanged at S2 — the canon question dominates the implementation question. Layer-misplacement of `compute.py` itself is captured in Finding 14 / migration plan.
**Remediation pattern:** canon decision first; then either drop, rename, or migrate to the correct layer in `edcm`.
**hmmm:** unresolved — which layer `P` belongs to once L1/L2/L3 are separated, or whether `P` is canon-divergent and should be dropped.

### Finding 07 — A_MATRIX declared but not consumed

**Original severity (audit session):** S2
**Re-graded severity against canon:** S1
**Canonical home:** L1 (the linear map `M_t = A·φ` is the L1 definition)
**File(s):** `Backend/src/edcmbone/metrics/matrix.py`, `Backend/src/edcmbone/metrics/compute.py`
**Description:** `metrics/matrix.py` defines `A_MATRIX` and claims `M_t = A·φ`. `compute.py` hardcodes the same weights inline. A_MATRIX is documentation-shaped-as-Python; no code consumes it. Changing A_MATRIX has no effect.
**Why severity changed (if it did):** rose from S2 to S1 because A_MATRIX is the **canonical L1 contract** under held canon. A canon contract that is unwired is a load-bearing lie. Combined with the fact that both files are layer-misplaced (belong in `edcm/arc_style/`), this is a structural defect, not a cleanup.
**Remediation pattern:** wire `compute.py` (or its `edcm/arc_style/` successor) through `A_MATRIX` so the canonical map is the only source of L1 weights; then migrate both files upstream.
**hmmm:** unresolved — whether A_MATRIX should remain a single weights matrix or split per Arc Style metric once L1 is canonically pinned.

### Finding 08 — `A_MATRIX["E"]` references a Layer 1 metric, not a primitive

**Original severity (audit session):** S2
**Re-graded severity against canon:** S1
**Canonical home:** L1
**File(s):** `Backend/src/edcmbone/metrics/matrix.py`
**Description:** If A maps L0 primitives → L1 outputs, then A's columns are primitives. `A["E"]` referencing an L1 metric is layer-mixing inside the matrix itself.
**Why severity changed (if it did):** rose from S2 to S1 because this is a direct violation of the held L1 contract `M_t = A·φ` where φ is the L0 primitive vector. The matrix cannot reference its own outputs.
**Remediation pattern:** fix the matrix to use only L0 primitive columns; resolve via the same migration that wires A_MATRIX (Finding 07).
**hmmm:** unresolved — whether `E` here is a misnamed primitive or a genuinely L1-referencing entry that needs to be relocated to a separate L2 composite.

### Finding 09 — κ range mismatch

**Original severity (audit session):** S2
**Re-graded severity against canon:** S3
**Canonical home:** crosses L1 (matrix doc) and L3 (PROJECTION_MAP["DA"])
**File(s):** `Backend/src/edcmbone/metrics/matrix.py` (docstring), `Backend/src/edcmbone/metrics/compute.py::energy_step` (clamp), `Backend/src/edcmbone/metrics/projection.py::PROJECTION_MAP["DA"]`
**Description:** `matrix.py` docstring says κ is unbounded ≥ 0. `energy_step` clamps κ to [0,1]. `PROJECTION_MAP["DA"]` requires [0,1]. Code is correct; docs are wrong.
**Why severity changed (if it did):** dropped to S3 — pure docstring drift, no runtime effect. Layer-misplacement of the affected files is captured in the migration plan, not in this finding's severity.
**Remediation pattern:** fix docstring in-place; migrate as part of L1/L3 migration phases.
**hmmm:** unresolved — whether canonical κ range is genuinely [0,1] (matching code + projection) or whether the projection map is the one in error.

### Finding 10 — `compress.py` lossless-claim false

**Original severity (audit session):** S2
**Re-graded severity against canon:** S2
**Canonical home:** L0 (lossless codec for L0 data)
**File(s):** `Backend/src/edcmbone/compress.py::_dict_to_tok`
**Description:** `_dict_to_tok` sets `entry={}` on decode. Docstring claims lossless round-trip; entry field is discarded. Existing tests check `bone_count` matches but do not verify entry preservation.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** in-place fix in edcmbone — either preserve entry on encode/decode, or correct the docstring to declare which fields are lossless. Add round-trip regression test (Finding 32).
**hmmm:** unresolved — whether canonical L0 compression must preserve `entry` byte-for-byte or whether `entry` is reconstructible from other preserved fields.

### Finding 11 — Affix strip over-fires

**Original severity (audit session):** S2
**Re-graded severity against canon:** S2
**Canonical home:** L0
**File(s):** `backend/src/edcmbone/parser/turns_rounds.py::_BoneClassifier`, `core/operator/matcher.py::match_affixes`
**Description:** Both implementations strip affixes greedily without validating residual is a real stem. "uncle" → strip "un-" → "cle" → emits un-family bone. False positives in PKQTS family counts propagate to every downstream layer.
**Why severity changed (if it did):** unchanged. L0 bug; remediation is in-place.
**Remediation pattern:** in-place fix — add stem-validity check or maintain a stop-list of false-positive stems. Add affix false-positive regression test (Finding 33).
**hmmm:** unresolved — whether stem validity is checked against a wordlist, a morphological analyzer, or a hand-curated stop-list.

### Finding 12 — Backend parser doesn't exclude SYS/TOOL from round anchoring

**Original severity (audit session):** S2
**Re-graded severity against canon:** S2
**Canonical home:** L0
**File(s):** `Backend/src/edcmbone/parser/turns_rounds.py`, `core/parsing/round_builder.py`
**Description:** Refactor `core/parsing/round_builder.py` excludes SYS/TOOL from round anchoring; Backend production parser does not. Drift between two L0 implementations.
**Why severity changed (if it did):** unchanged. L0 drift, but see Finding 14 — the existence of two parallel parsers is the deeper issue.
**Remediation pattern:** resolved by parallel-parser consolidation in Phase 1 of the migration plan. Whichever parser is chosen, SYS/TOOL exclusion is canonical.
**hmmm:** unresolved — whether SYS/TOOL exclusion is canonical (refactor side) or whether the Backend behavior reflects a deliberate canon decision.

### Finding 13 — Backend tokenizer splits contractions; refactor keeps them whole

**Original severity (audit session):** S2
**Re-graded severity against canon:** S2
**Canonical home:** L0
**File(s):** `Backend/src/edcmbone/parser/turns_rounds.py` vs `core/parsing/tokenizer.py`
**Description:** Concrete drift between two L0 tokenizer implementations on a fundamental tokenization decision.
**Why severity changed (if it did):** unchanged. Same shape as Finding 12 — drift resolved by Finding 14.
**Remediation pattern:** resolved by parallel-parser consolidation.
**hmmm:** unresolved — canonical L0 tokenization rule for ASCII contractions. The `stats.py` regression test (Finding 04) asserts they stay whole, which suggests the refactor side is canonical, but `stats.py` is not necessarily the source of truth.

### Finding 14 — Parallel parser implementations

**Original severity (audit session):** S2
**Re-graded severity against canon:** S1
**Canonical home:** L0
**File(s):** `Backend/src/edcmbone/parser/turns_rounds.py`, `core/parsing/{turn_builder,round_builder,tokenizer,normalizer}.py`
**Description:** Two parallel real L0 implementations with no drift-control contract. Findings 12 and 13 are instances; more drift will accumulate.
**Why severity changed (if it did):** rose from S2 to S1. Two canonical L0 parsers cannot coexist; Bridge's correlation contract (Operator output ↔ Behavioral output) becomes meaningless if the upstream L0 stream is non-deterministic across consumers.
**Remediation pattern:** Phase 1 of the migration plan — pick one canonical L0 parser. Document the drift-control contract for the other (deletion, archive, or test-only reference).
**hmmm:** unresolved — which parser wins consolidation. Refactor side has tokenizer/normalizer separated (more architecturally sound); Backend side has the 87-test suite (more verification). hmmm flagged in migration plan.

### Finding 15 — `hmm` (2m) vs `hmmm` (3m) drift

**Original severity (audit session):** S2
**Re-graded severity against canon:** S1
**Canonical home:** canon-independent (canon-enforcement, applies across all layers)
**File(s):** `engine.py`, `operator_extractor.py`, `bridge_engine.py`, `behavioral_metrics.py`, `tests/run_all.py`
**Description:** Five files use `hmm` as dict key or print marker. Canon: `hmmm` (3m). Per held canon, absence of `hmmm` (or substitution of a 2m variant) is fail-closed.
**Why severity changed (if it did):** rose from S2 to S1 — held canon's hmmm-enforcement rule makes any 2m variant a canon violation, not stylistic drift.
**Remediation pattern:** in-place rename across all five files; add a test that scans the codebase for bare `hmm` outside of substring contexts. Mid-migration timing: must be done before any of these files migrate out of edcmbone, to avoid carrying the violation upstream.
**hmmm:** unresolved — whether `hmm` substrings inside larger tokens (e.g., a hypothetical `hmm_count`) are also violations or only standalone uses.

### Finding 16 — closed_tokens silent class collisions

**Original severity (audit session):** S2
**Re-graded severity against canon:** S3
**Canonical home:** L0
**File(s):** `closed_tokens.py`, `Backend/src/edcmbone/ucns/closed_tokens.py`
**Description:** `since`, `until`, `as` resolve to preposition; `that` resolves to determiner. Tests assert this — behavior is specified. But no diagnostic logging when a later-class entry is silently dropped.
**Why severity changed (if it did):** dropped from S2 to S3 — the behavior is canon-pinned via tests; the gap is observability, not correctness.
**Remediation pattern:** in-place — add diagnostic logging or structured warning at registration time.
**hmmm:** unresolved — whether silent overwrite is the canon behavior or merely the current implementation. If canon, no logging is needed; if not, logging plus possibly raising is needed.

### Finding 17 — HOST_CARRIER / hardcoded 32 fragile coupling

**Original severity (audit session):** S3
**Re-graded severity against canon:** S3
**Canonical home:** L0
**File(s):** `closed_tokens.py` (HOST_CARRIER=16 and hardcoded 32 in `_wrap_with_class`/`class_of`)
**Description:** Magic constants 16 and 32 coupled across functions without a single source of truth.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** in-place — extract named constants and use them throughout.
**hmmm:** none — straightforward cleanup.

### Finding 18 — Dead code

**Original severity (audit session):** S4
**Re-graded severity against canon:** S4
**Canonical home:** L0 / mixed
**File(s):** `closed_tokens.py` (`unit_obj`, `multiply` imported unused; `_class_anchor` defined never called; `CLASS_PUNCT_QUOTE = 12` reserved never used); `core/operator/operator_extractor.py` (`hyphen_compound_emission` imported but logic inlined); `core/behavioral/behavioral_metrics.py` or similar (`detect_list_growth_pattern` defined but never called); tokenizer dead fallback `if not toks`.
**Description:** Multiple instances of dead identifiers, unused imports, and never-called helpers.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** in-place cleanup pass; address after layer migration to avoid bikeshedding files that are moving.
**hmmm:** unresolved — `CLASS_PUNCT_QUOTE = 12` may be reserved-for-future-use rather than dead; check intent before removing.

### Finding 19 — WHITESPACE_TABLE possible space ↔ NBSP collision

**Original severity (audit session):** S3
**Re-graded severity against canon:** S3
**Canonical home:** L0 (whitespace normalization is sub-primitive)
**File(s):** `closed_tokens.py` (or wherever `WHITESPACE_TABLE` is defined)
**Description:** Possible byte-level collision between ASCII space (U+0020) and NBSP (U+00A0) as dict keys.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** verify byte-level locally with `od -c`; fix in-place if collision exists.
**hmmm:** unresolved — byte-level verification pending.

### Finding 20 — closed_tokens disk-flip claim without implementation

**Original severity (audit session):** S3
**Re-graded severity against canon:** S3
**Canonical home:** L0
**File(s):** `closed_tokens.py` (docstring), `ucns_v04.py`
**Description:** Docstring asserts a disk-flip behavior that has no corresponding implementation in `ucns_v04.py`.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** three options: find the test that verifies the claim, implement it, or remove the docstring claim.
**hmmm:** unresolved — whether the disk-flip behavior is canonical L0 (then implement) or aspirational (then remove the claim).

### Finding 21 — CanonLoader re-reads JSON on every construction

**Original severity (audit session):** S3
**Re-graded severity against canon:** S3
**Canonical home:** L0
**File(s):** `Backend/src/edcmbone/canon/loader.py`, callers in `metrics/compute.py`
**Description:** `compute_round` and `compute_transcript` create fresh `CanonLoader()` if `canon=None` → per-transcript JSON re-reads.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** in-place — cache loaded canon at module level or via lru_cache.
**hmmm:** none — pure performance.

### Finding 22 — canon/loader.py affix-section list hardcoded

**Original severity (audit session):** S3
**Re-graded severity against canon:** S3
**Canonical home:** L0
**File(s):** `Backend/src/edcmbone/canon/loader.py`
**Description:** New affix-section silently ignored because the section-list is hardcoded.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** in-place — discover sections from the JSON file rather than hardcoding.
**hmmm:** unresolved — whether the hardcoded section list is a canon-pin (intentional whitelist) or implementation laziness.

### Finding 23 — bridge_engine O(n²) Pearson prefix recomputation

**Original severity (audit session):** S3
**Re-graded severity against canon:** S3
**Canonical home:** sideways (Bridge)
**File(s):** `core/bridge/bridge_engine.py`, `core/bridge/math_utils.py`
**Description:** Online statistics recomputed from scratch each step; should use Welford-style accumulators → O(n).
**Why severity changed (if it did):** unchanged. Bridge layer lives sideways, not in the migration tree.
**Remediation pattern:** in-place algorithmic fix in whichever package Bridge ultimately lives in. Defer until Bridge's home is decided.
**hmmm:** unresolved — Bridge's physical home (see migration plan §E and hmmm there).

### Finding 24 — `prev_energy` unused parameter plumbed through compute_transcript

**Original severity (audit session):** S4
**Re-graded severity against canon:** S4
**Canonical home:** crosses L1/L2/L3 (the `compute.py` orchestrator)
**File(s):** `Backend/src/edcmbone/metrics/compute.py::energy_step`, `compute_transcript`
**Description:** `prev_energy` is plumbed but unused.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** remove the parameter — but only after the orchestrator migrates to `edcm`, to avoid editing files that are moving.
**hmmm:** none — straightforward cleanup; sequencing only.

### Finding 25 — `_compute_D` docstring stale

**Original severity (audit session):** S4
**Re-graded severity against canon:** S4
**Canonical home:** L1 or L2 Behavioral slice (uncertain — see migration plan §F)
**File(s):** `Backend/src/edcmbone/metrics/compute.py::_compute_D`
**Description:** Docstring claims "low bone density as proxy" but implementation uses `1 - cosine_sim`.
**Why severity changed (if it did):** unchanged. Pure docstring drift.
**Remediation pattern:** in-place docstring fix; defer until layer migration.
**hmmm:** unresolved — which of the docstring and the implementation reflects canon intent for D.

### Finding 26 — Unused imports in compute.py

**Original severity (audit session):** S4
**Re-graded severity against canon:** S4
**Canonical home:** orchestrator (crosses L1/L2/L3)
**File(s):** `Backend/src/edcmbone/metrics/compute.py`
**Description:** `Counter`, `math`, `BoneToken` imported but not used.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** remove during cleanup pass; defer until layer migration.
**hmmm:** none.

### Finding 27 — RoundMetrics integer defaults declared as float

**Original severity (audit session):** S4
**Re-graded severity against canon:** S4
**Canonical home:** L1/L2 (RoundMetrics is a layer-mixed container; will split during migration)
**File(s):** `Backend/src/edcmbone/metrics/compute.py::RoundMetrics`
**Description:** `round_index`, `token_count`, `bone_count` default to `0.0` (float) — should be int.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** in-place type fix.
**hmmm:** none.

### Finding 28 — gini_tbf dead Counter

**Original severity (audit session):** S4
**Re-graded severity against canon:** S4
**Canonical home:** L3 (TBF is in the projection set)
**File(s):** `Backend/src/edcmbone/metrics/projection.py` or `compute.py` (`gini_tbf`)
**Description:** `counts = Counter(t.token_count for t in turns)` built then discarded.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** delete the dead line during cleanup.
**hmmm:** none.

### Finding 29 — `broken_return` not wrapped in clamp()

**Original severity (audit session):** S4
**Re-graded severity against canon:** S4
**Canonical home:** L2 (risk composites)
**File(s):** `Backend/src/edcmbone/metrics/risk.py` (risk functions)
**Description:** Only risk function not wrapped in `clamp()`. Inconsistency-not-bug.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** in-place consistency fix or document the intentional asymmetry.
**hmmm:** unresolved — whether the lack of clamp is intentional (range is naturally bounded for this risk) or an oversight.

### Finding 30 — fire_alerts only handles direction="above"

**Original severity (audit session):** S4
**Re-graded severity against canon:** S4
**Canonical home:** L3
**File(s):** `Backend/src/edcmbone/metrics/projection.py::fire_alerts`
**Description:** Future `"below"` thresholds would silently miss.
**Why severity changed (if it did):** unchanged.
**Remediation pattern:** in-place — either implement both directions or raise on unknown direction.
**hmmm:** unresolved — whether bidirectional alerts are canonical L3 or whether `"above"`-only is canon-pinned.

### Finding 31 — behavioral_metrics `ucns_store` not plumbed

**Original severity (audit session):** S3
**Re-graded severity against canon:** S2
**Canonical home:** Behavioral slice (L1/L2 mixed — see migration plan §F)
**File(s):** `core/behavioral/behavioral_metrics.py`, `compute_behavioral_windows`
**Description:** `ucns_store` parameter exists but is not plumbed → the UCNS code path never actually runs.
**Why severity changed (if it did):** rose from S3 to S2 — a non-running canonical code path is more severe than dead local code because it is silently invisible to all consumers. The UCNS integration is one of the two named upstream dependencies of the future `edcm` package; silently disabling it is a structural defect.
**Remediation pattern:** plumb the parameter through, add a test that asserts the UCNS path is exercised. Defer until layer migration places the file in its canonical home.
**hmmm:** unresolved — whether UCNS is L0 territory (alongside edcmbone) or upstream in the future `edcm` package. Affects where this plumbing lives after migration.

### Finding 32 — No regression test for BoneToken.entry round-trip

**Original severity (audit session):** test-gap
**Re-graded severity against canon:** S3 (test gap covering an S2 bug — Finding 10)
**Canonical home:** L0
**File(s):** `Tests/test_backend.py` (additions)
**Description:** Compress round-trip is asserted on `bone_count` only; `entry` discard is not caught by tests.
**Remediation pattern:** add unit test alongside Finding 10's fix.
**hmmm:** none.

### Finding 33 — No test for affix false positives

**Original severity (audit session):** test-gap
**Re-graded severity against canon:** S3 (covers Finding 11)
**Canonical home:** L0
**File(s):** test suite
**Description:** "uncle", "redo", "linking", etc. should not trigger affix-family emissions.
**Remediation pattern:** add parametrized test alongside Finding 11's fix.
**hmmm:** unresolved — which canonical wordlist or stop-list seeds the test cases (depends on Finding 11's resolution path).

### Finding 34 — No test for monologue → degenerate single-turn rounds

**Original severity (audit session):** test-gap
**Re-graded severity against canon:** S3
**Canonical home:** L0 (parser)
**File(s):** test suite
**Description:** Round-builder behavior on single-speaker monologue inputs is untested.
**Remediation pattern:** add test against whichever parser wins consolidation (Finding 14).
**hmmm:** unresolved — whether canonical behavior on monologue is "one round per turn" or "all turns one round" or "no rounds emitted."

### Finding 35 — No test for SYS/TOOL exclusion behavior

**Original severity (audit session):** test-gap
**Re-graded severity against canon:** S3
**Canonical home:** L0
**File(s):** test suite
**Description:** Neither parser has a test pinning SYS/TOOL exclusion behavior, which is itself disputed (Finding 12).
**Remediation pattern:** add test after Finding 12's canon decision.
**hmmm:** unresolved — pin canon first, then test.

### Finding 36 — No test for smart-apostrophe parser input

**Original severity (audit session):** test-gap
**Re-graded severity against canon:** S3
**Canonical home:** L0
**File(s):** test suite
**Description:** Parser behavior on smart-quoted contractions is untested, despite Finding 03's normalizer no-op.
**Remediation pattern:** add test alongside Finding 03 fix.
**hmmm:** none.

### Finding 37 — No test for normalizer no-op replace bug

**Original severity (audit session):** test-gap
**Re-graded severity against canon:** S3
**Canonical home:** L0
**File(s):** test suite
**Description:** Direct test for `normalize_text_for_matching` byte-level transformation.
**Remediation pattern:** add test alongside Finding 03 fix.
**hmmm:** none.

### Finding 38 — No cross-pipeline convergence test

**Original severity (audit session):** test-gap
**Re-graded severity against canon:** S2
**Canonical home:** L0 (drift-control between parallel parsers)
**File(s):** test suite
**Description:** No test asserts that Backend production output and refactor engine output agree on the same transcript.
**Why severity changed (if it did):** rose from test-gap to S2 because convergence is the only way to detect Findings 12/13-class drift between parallel parsers without re-running the audit. Without it, Bridge's correlation contract has no guard.
**Remediation pattern:** add convergence test before parallel-parser consolidation, as the regression net for whichever side gets retired. Then drop the test once one side is gone.
**hmmm:** unresolved — what tolerance the convergence test enforces (byte-equal, structural-equal, metric-equal-within-ε).

### Finding 39 — Refactor pipeline has only 1 smoke test + 1 golden-drift harness

**Original severity (audit session):** test-gap
**Re-graded severity against canon:** S3
**Canonical home:** L0 (refactor side) and upstream `edcm` (post-migration)
**File(s):** `core/` and its tests
**Description:** No per-component tests parallel to the Backend 87-test suite.
**Remediation pattern:** if refactor parser wins consolidation, backfill tests before migration begins; if Backend parser wins, refactor side is archived and the tests-gap is moot.
**hmmm:** unresolved — depends on Finding 14's consolidation decision.

---

## Summary table — re-graded findings

Sorted by re-graded severity then canonical home.

| # | Title | Re-graded | Canonical home |
|---|-------|-----------|----------------|
| 01 | Case-collision dirs | S1 | canon-independent |
| 02 | Backend not installable | S1 | canon-independent |
| 03 | Normalizer no-op | S1 | L0 |
| 04 | Parser apostrophe regex unverified | S1 | L0 |
| 14 | Parallel parser implementations | S1 | L0 |
| 15 | hmm (2m) vs hmmm (3m) drift | S1 | canon-independent |
| 05 | F-metric double definition | S1 | L1/L2 + Bridge |
| 07 | A_MATRIX declared but not consumed | S1 | L1 |
| 08 | A_MATRIX["E"] references L1 metric | S1 | L1 |
| 06 | `P` out of 9-list | S2 | uncertain (L1 or L2) |
| 10 | compress.py lossless-claim false | S2 | L0 |
| 11 | Affix strip over-fires | S2 | L0 |
| 12 | Backend parser SYS/TOOL anchoring | S2 | L0 |
| 13 | Backend vs refactor tokenizer contraction drift | S2 | L0 |
| 31 | behavioral_metrics ucns_store not plumbed | S2 | Behavioral (L1/L2) |
| 38 | No cross-pipeline convergence test | S2 | L0 |
| 09 | κ range mismatch | S3 | L1 / L3 |
| 16 | closed_tokens silent class collisions | S3 | L0 |
| 17 | HOST_CARRIER / hardcoded 32 | S3 | L0 |
| 19 | WHITESPACE_TABLE collision risk | S3 | L0 |
| 20 | disk-flip claim w/o implementation | S3 | L0 |
| 21 | CanonLoader re-reads JSON | S3 | L0 |
| 22 | canon/loader.py affix-section hardcoded | S3 | L0 |
| 23 | bridge_engine O(n²) | S3 | sideways (Bridge) |
| 32 | No BoneToken.entry round-trip test | S3 | L0 |
| 33 | No affix false-positive test | S3 | L0 |
| 34 | No monologue round-builder test | S3 | L0 |
| 35 | No SYS/TOOL exclusion test | S3 | L0 |
| 36 | No smart-apostrophe parser test | S3 | L0 |
| 37 | No normalizer no-op test | S3 | L0 |
| 39 | Refactor pipeline test-thin | S3 | L0 / upstream |
| 18 | Dead code | S4 | mixed |
| 24 | `prev_energy` unused param | S4 | L1/L2/L3 orchestrator |
| 25 | `_compute_D` docstring stale | S4 | L1 or L2 |
| 26 | Unused imports in compute.py | S4 | orchestrator |
| 27 | RoundMetrics int defaults as float | S4 | L1/L2 |
| 28 | gini_tbf dead Counter | S4 | L3 |
| 29 | broken_return not clamped | S4 | L2 |
| 30 | fire_alerts only direction="above" | S4 | L3 |

---

## Findings where four-layer canon does not determine the answer

The findings below were marked `hmmm:` unresolved because the held canon (L0 + L1 = `M_t = A·φ` + L2 risk composites + L3 = 6 agent metrics CM/DA/DRIFT/DVG/INT/TBF + Bridge sideways) does not yet pin the decision. Surfaced for Erin to resolve before remediation can proceed cleanly:

- **Finding 01** — canonical directory casing per pair.
- **Finding 02** — whether `ucns_v04.py` belongs in edcmbone at all.
- **Finding 05** — canonical operationalization of `F` at L1 vs L2.
- **Finding 06** — which layer `P` belongs to, or whether `P` is canon-divergent.
- **Finding 07** — single vs split A_MATRIX once L1 is canonically pinned.
- **Finding 08** — whether `A_MATRIX["E"]` is a misnamed primitive or genuinely L2-bound.
- **Finding 09** — canonical κ range source of truth.
- **Finding 10** — whether `entry` is byte-preserve-required or reconstructible.
- **Finding 12** — canonical SYS/TOOL anchoring behavior.
- **Finding 13** — canonical L0 tokenization rule for ASCII contractions.
- **Finding 14** — which parser wins consolidation.
- **Finding 16** — canonical class-collision behavior in closed_tokens.
- **Finding 20** — canonical disk-flip status.
- **Finding 22** — canonical affix-section enumeration policy.
- **Finding 29** — `broken_return` intentional asymmetry or oversight.
- **Finding 30** — bidirectional alerts in canonical L3 or `"above"`-only.
- **Finding 31** — UCNS canonical home (L0-adjacent or upstream).
- **Finding 34** — canonical monologue round-builder behavior.
- **Finding 39** — depends on Finding 14.

---

## Apparent contradictions between findings

- **Finding 14 vs Findings 12/13/38** — consolidating the parallel parsers (14) implies retiring one of them. But the convergence test in Finding 38 needs both alive to detect drift. Sequencing: introduce 38's convergence test **first** (so the retiring side's death is regression-checked), then consolidate per 14, then drop 38's convergence test once the retiring side is gone. Findings 12 and 13 are subsumed by 14's resolution.
- **Finding 07 vs Finding 08** — Finding 07 says wire `compute.py` through `A_MATRIX`. Finding 08 says `A_MATRIX["E"]` is layer-mixed. Wiring without first fixing the layer-mix would propagate the L1-referencing-L1 violation. Sequence: 08 before 07.
- **Finding 02 vs everything else** — Backend's non-installability (02) means all "in-place fix in `Backend/src/edcmbone/`" remediations are conditional on the package becoming installable first. If 02 is not resolved Phase 0, every other in-place fix is shipping into a non-shippable package.

hmmm: this contradictions list is non-exhaustive; a second pass after Erin resolves the canon-pending `hmmm`s above will likely surface more.

---

## hmmm — global

hmmm: re-grading was performed against held canon as understood from the handoff brief, without re-reading every cited file byte-for-byte. Findings 04, 19 (apostrophe-regex byte-verification, NBSP collision byte-verification) and the disk-flip implementation search (Finding 20) explicitly require local byte-level / repo-wide verification that has **not** been done in this re-grading session. Severity could shift on actual inspection.

hmmm: the four-layer canon held in this re-grading does not enumerate L1's 11 Arc Style metrics or L2's risk composite names; per the brief's "do not enumerate" rule, every layer assignment of a specific metric (`F`, `P`, `D`, `E`, `κ`) is grounded only in the file location and the linear-map contract, not in a canonical letter-to-layer table. A canonical table would let several `hmmm:` markers above resolve themselves.

hmmm: end of document.
