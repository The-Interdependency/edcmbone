# EDCM Canon v2 Proposal — Three-Layer Architecture, Lensing-as-Structure

**Status:** Proposal, not yet frozen  
**Authored:** 2026-05-01  
**Source thread:** Iterative architectural design session, Claude Project conversation  
**Target landing:** `canon_eng/canon_v2_proposal.md` in The-Interdependency/edcmbone  
**Dependency context:** interdependent-lib will become the primary dependency aggregating PCEA, edcmbone, ZFAE, PCNA, PTCA, PCTA — each maintained as a zero-dependency standalone library

---

## 0) Status of Prior Canon

Canon v1 (`canon_eng/spec.md`, `canon_eng/spec_hard_freeze_appendix_v1.md`, `canon_eng/behavioral_formulas_v1.md`, all `*_schema_v1.json`, `bones_v1.json`, `affixes_v1.json`, `behavioral_markers_v1.json`) remains frozen and authoritative for the two-layer system it describes. This proposal extends, it does not overwrite. Backward semantic compatibility is preserved per the canon's own evolution constraint (EDCM metrics §"Evolution constraint": old definitions are archived, not overwritten).

**What v1 specifies and freezes:**

- Operator-EDCM (5D, P/K/Q/T/S, bones-only, Σ_f O_f = 1)
- Behavioral-EDCM (9 metrics: C, R, D, N, L, O, F, E, I)
- Bridge layer (correlations + divergence flags, read-only)
- Parsing convention (turns, rounds, initiator-return closure)
- Windowing (W_turn(k=8) for Operator, W_round(m=4) for Behavioral)
- Bone inventory and affix inventory
- Behavioral markers (26 markers across 9 metrics — actual count, not the previously-claimed ~186)

**What v1 leaves open:**

- C (Constraint Strain) named but never given a computable formula
- D, L, O, I named but flesh- or marker-substrate computability never specified
- No third measurement layer
- No trajectory metrics (state-within-window only)

---

## 1) Decisions Locked in This Proposal

### 1.1 Three-layer architecture

| Layer | Substrate | Counts | Embedder | Conservation |
|---|---|---|---|---|
| Operator (bones) | closed-class words, affixes, select punctuation | 5D (P,K,Q,T,S) | UCNS (BoneEmbedder) | Σ_f O_f = 1 (frozen, v1) |
| Behavioral (markers) | curated phrasal markers | 11D (snapshot 9 + trajectory 2) | none — embedding-free | unbounded (frozen, v1) |
| Content (flesh) | open-class lexical content, per claim | 10D (4 status + 6 rating) | ZFAE (ContentEmbedder) | TBD per layer |

The substrate-to-embedder allocation is the structural kernel of v2: each layer gets exactly the embedding machinery its substrate demands. Bones are a finite alphabet — UCNS (Mobius-disk-recursive-epicycles) is its native topology. Markers are curated phrasal patterns — deterministic match, no embedding. Flesh is unbounded vocabulary — ZFAE handles inference.

### 1.2 Lensing-as-structure principle

Where metric names overlap across layers (initially: C, R, N, F, E share names between Behavioral and Content), each layer produces an independent reading. The disagreement between readings is itself a diagnostic signal, mediated by the Bridge layer.

This extends the polarity-balance principle from canon v1 (if the negative pole of a bone is included, the affirmative pole must be too) into the measurement architecture itself. Apparent contradictions across layers are intentional design features — different lensing of the same information, not competing approaches.

### 1.3 Behavioral extends to 11D

Behavioral splits into:

- **Snapshot sub-vector (9D):** C, R, D, N, L, O, F, E, I — frozen v1, marker-computed, state within window
- **Trajectory sub-vector (2D):** M (Motion), B (Basin) — temporal metrics across windows

Letter codes: Motion uses M (Progress was the original GPT-module name; renamed M to avoid collision with Operator's P=Polarity, which is frozen). Basin uses B.

### 1.4 Three parallel paths for trajectory metrics (M, B)

Iteration discerns which is most effective per the canon's existing falsification framework (predictive asymmetry, repeatability, constraint robustness, non-inversion). Two outcomes survive:

- One path dominates → use it; archive others as falsified-but-preserved
- Multiple paths complement → keep two or three, emit all readings, the disagreement becomes a coupling-layer signal in itself

**Path (a) — Curated markers.** Two new marker sets in `behavioral_markers_v1.json` (or `_v2.json`): `motion_markers`, `basin_markers`. Same architecture as the existing 26 markers. Marker-pure, transcript-deterministic.

**Path (b) — Derivatives.** M and B computed as functions of the 9D snapshot vector across windows. M = first-derivative-like delta over snapshot. B = stability/attractor check on snapshot trajectory. No new markers, no new substrate; pure structural function of the existing layer.

**Path (c) — Embedding-routed.** M and B handled via ZFAE on surrounding flesh context. Note: markers themselves have no native embedder, so this path uses the Content layer's embedder applied to the flesh adjacent to marker hits. Less natural than (a) or (b); may be unproductive.

Path (b) appears most TIW-coherent on its face (Motion and Basin become structural functions of existing measurements rather than independent inputs), but selection is empirical, not architectural.

### 1.5 Content layer schema (10D per claim)

**Status flags (4, categorical):**

- `truth_status`: `true` | `untrue` | `unknown`
- `verification_status`: `verified` | `unverified` | `unverifiable`
- `foundation_status`: `axiom` | `derivation` | `asserted_without_foundation`
- `speech_act`: `uttered` | *(additional values TBD — see §3)*

**Ratings (6, scalar):**

- `utility`
- `clarity`
- `focus`
- `aesthetic`
- `psychological`
- `epistemic`

Range and rating-frame anchors: see §3 (open questions).

### 1.6 Three-way Bridge

Bridge becomes ternary:

- O ↔ B (existing canon)
- O ↔ C (new — structure-without-content divergence)
- B ↔ C (new — dynamics-without-claim divergence)

Each pair produces correlations (rolling windows) and divergence flags. Bridge never modifies any layer — this rule from v1 carries forward unchanged.

### 1.7 Zero-dependency constraint and protocol-based dependency inversion

edcmbone, UCNS, ZFAE, PCNA, PTCA, PCTA, PCEA each ship as standalone zero-dependency libraries. edcmbone never imports an embedder. It defines Protocol classes — `BoneEmbedder`, `ContentEmbedder`, `ClaimExtractor` — that interdependent-lib wires to concrete UCNS / ZFAE / etc. implementations.

This makes edcmbone-as-canon stay pure measurement (per existing v1 dependency principle: "edcmbone is pure measurement, ZFAE is model-dependent inference, A0 orchestrates both"), even when measurement requires embedding. The library declares the shape of an embedder; the application wires the implementation.

### 1.8 The C formula advance is preserved, repositioned

The GPT-generated `edcm_metrics.py` introduced the first computable formula for C (Constraint Strain), which v1 names but never defines. That module operated on flesh substrate, which initially appeared to contradict canon (canon's Operator layer discards flesh). v2 resolves: the formula migrates from flesh-domain to marker-domain for the Behavioral C, and its flesh-domain reading lives in the Content layer (since C appears in both under the lensing principle). The canonical advance is "C is computable" — that survives. The substrate-specific implementations multiply rather than conflict.

The module's Progress and Basin become seed material for trajectory paths (b) — the derivative path — since their original formulas are most naturally translated as functions of an underlying state vector.

---

## 2) Repository Layout

### 2.1 The-Interdependency/edcmbone (this canon repo)

The library code lives at `edcmbone/edcmbone/` (the nested subpackage path that already exists). Application surface (`frontend/`, `backend/`, `engine.py`) imports the library; library never imports the application.

Proposed v2 structure (extends existing):

```
edcmbone/edcmbone/
├── operator/              # frozen v1 — bones layer, P/K/Q/T/S
│   ├── tokenize.py
│   ├── morph.py
│   ├── count.py
│   └── aggregate.py
├── behavioral/
│   ├── snapshot/          # frozen v1 9 metrics, marker-computed
│   │   ├── markers.py
│   │   └── metrics.py
│   └── trajectory/        # NEW — Motion, Basin
│       ├── markers_a.py   # path (a)
│       ├── derivative_b.py # path (b)
│       ├── embedding_c.py  # path (c)
│       └── select.py       # config flag: a | b | c | ensemble
├── content/               # NEW — flesh layer
│   ├── claim_extractor.py # uses ClaimExtractor protocol
│   ├── status.py          # 4 categorical flags
│   ├── rating.py          # 6 scalar ratings
│   ├── vector.py          # 10D assembly
│   └── window.py
├── bridge/
│   ├── correlate.py       # extended to ternary
│   └── divergence.py      # extended to ternary
└── protocols/             # NEW — interfaces, no implementations
    ├── bone_embedder.py
    ├── content_embedder.py
    └── claim_extractor.py
```

### 2.2 erinepshovel-code/interdependent-lib (the aggregator)

interdependent-lib becomes the primary dependency that wires everything:

```
interdependent_lib/
├── edcm/    # imports edcmbone (zero-dep), wires UCNS as BoneEmbedder, ZFAE as ContentEmbedder
├── pcea/    # imports PCEA (zero-dep)
├── pcna/    # imports PCNA (zero-dep)
├── pcta/    # imports PCTA (zero-dep)
└── ptca/    # imports PTCA (zero-dep)
```

Aggregator owns wiring; no library owns its consumers. Only interdependent-lib knows the full topology.

### 2.3 Canonical-mirror status

Per the canonical-ownership principle (canon must always reside in an individual's hands; orgs are mirrors only): once interdependent-lib is structurally complete, it should be mirrored to `wayseer00/interdependent-lib` (which currently does not exist in the audit). This is a structural gap to close, not part of v2 spec proper, but noted here so it's not lost.

---

## 3) Open Questions (Hard-Decide Before Freeze)

These must resolve before v2 freezes. Provisional defaults are offered where reasonable.

### 3.1 Speech-act enum completion

`speech_act` was sketched as starting with `uttered`. Candidates for additional values:

- `referenced` — the claim is mentioned but not advanced as the speaker's own
- `quoted` — direct quotation of another source
- `implied` — claim is structurally entailed but not explicitly stated
- `negated_utterance` — the claim is denied / the negation is what was uttered
- `hypothetical` — claim is offered conditionally / as supposition

**Provisional default:** `uttered | referenced | quoted | implied | negated | hypothetical` (6 values). Override before freeze.

### 3.2 Rating-frame anchors

Each of the 6 scalar ratings needs a reference frame for reproducibility:

- `utility`: to whom, for what?
- `clarity`: to which audience?
- `focus`: relative to what topic / what scope?
- `aesthetic`: by whose criterion?
- `psychological`: for whom — the utterer or the receiver?
- `epistemic`: against what standard?

**Provisional default:** Single shared frame — "to the receiver, in the context of this conversation's stated topic." This makes the ratings receiver-relative and conversation-scoped, which is reproducible because the receiver and topic are both transcript-determinable. Override if a different anchor is desired (e.g., utterer-relative, world-anchored, third-party-judge-relative).

### 3.3 Rating type and range

- Signed [-1, 1]?
- Unsigned [0, 1]?
- Ordinal bins (e.g., {very_low, low, mid, high, very_high})?

The choice constrains the coupling-layer math (ratio vs. signed divergence vs. cosine).

**Provisional default:** Unsigned [0, 1], continuous. Cleanest for ratio and cosine math; signed divergence can still be computed via difference. Override if signed semantics matter for a specific rating (e.g., `aesthetic` might want signed for "actively ugly" vs "merely lacking beauty").

### 3.4 Epistemic rating vs status flag overlap

The `epistemic` rating sits beside `truth_status`, `verification_status`, `foundation_status`. Three possibilities:

- (a) `epistemic` is a summary scalar over the three status flags (compositional)
- (b) `epistemic` is independent — measures something like confidence-warrantedness or knowledge-quality apart from truth/verification/foundation
- (c) The three status flags are subsumed under `epistemic` and removed

**Provisional default:** (b) — independent dimension. Status flags are categorical claims about the proposition's logical/evidential structure; the epistemic rating measures knowledge-quality of the assertion itself (warranted? well-grounded? appropriately hedged?). Override if (a) or (c) is preferred.

### 3.5 Content layer conservation

Operator has Σ_f O_f = 1. Behavioral has no conservation (snapshot vector is unbounded). What about Content?

**Provisional default:** No conservation. Content is per-claim, with status flags categorical and ratings independent. A window-aggregate Content vector can be averaged or distributed-counted, but no Σ = 1 invariant is enforced. Override if a normalized form is desired.

### 3.6 BoneEmbedder protocol shape

What does edcmbone need from UCNS? Possibilities:

- Vector-per-bone-token (ignoring context)
- Vector-per-bone-in-context (sequence-aware)
- Distance/similarity function only (no explicit vectors exposed)
- All of the above

**Provisional default:** Vector-per-bone-in-context, with a distance method. Sequence-aware because the bone's role often depends on neighboring bones (e.g., "not" preceding "and" vs. preceding "the"). Override if UCNS's actual API constrains this differently.

### 3.7 ContentEmbedder protocol shape

Probably needs:

- `extract_claims(text) -> list[Claim]`
- `embed_claim(claim) -> vector`
- Tagging functions for the 4 status flags
- Scoring functions for the 6 ratings

Whether these are one protocol or two (`ClaimExtractor` + `ContentEmbedder` as separate) is an API question.

**Provisional default:** Two protocols. `ClaimExtractor` extracts and segments. `ContentEmbedder` tags and rates. Cleaner separation of concerns; allows different implementations of each.

### 3.8 Marker-as-third-substrate optionality

Behavioral is currently embedding-free by design. Should the spec say "embedding-free always" or "embedding-free by default, with optional `MarkerEmbedder` for future extensibility"?

**Provisional default:** Embedding-free always. Markers are deliberately curated; introducing an embedder for them muddles the substrate-to-embedder allocation that is v2's structural kernel. If marker-embedding becomes useful later, it can be added as a v3 amendment.

---

## 4) Falsification Anchors for Iteration

Per EDCM metrics §"Validation criteria" and §"Falsification pathways", v2 additions must remain falsifiable. Specifically:

- **Trajectory paths (a/b/c):** evaluated via predictive asymmetry on a test corpus. A path that flags trajectory shifts before behavioral failure with statistical significance survives; one that does not is archived.
- **Content layer:** evaluated via repeatability — independent runs (or independent ZFAE inferences) on the same transcript should converge on similar status flags and ratings within a stated tolerance.
- **Lensing-as-structure:** evaluated by demonstrating that disagreement between layer readings carries information beyond either reading alone. If layer disagreement reduces to noise, the lensing principle is empirically empty even if architecturally elegant.

A test corpus is required before any of these are evaluated. Test corpus design is the next concrete deliverable after v2 spec freeze.

---

## 5) Migration Notes

### 5.1 Existing code in canon_eng/ and edcmbone/

The existing `canon_eng/spec.md` and `canon_eng/spec_hard_freeze_appendix_v1.md` are v1-frozen and stay. v2 lands as a sibling document (`canon_v2_proposal.md` → eventually `canon_v2_freeze.md`). Schema files (`*_schema_v1.json`) get v2 siblings as needed (`behavioral_schema_v2.json` for the 11D extension; `content_schema_v1.json` as a new file).

### 5.2 The GPT-generated edcm_metrics.py module

Treat as seed material, not as canonical code. Its C formula migrates to marker-domain (Behavioral C); its Progress/Basin formulas migrate to trajectory path (b). The module itself does not land in the library; it is referenced as a research artifact.

### 5.3 interdependent-lib finalization checklist

Per the user's stated goal: finalize PCEA, edcmbone, ZFAE, PCNA, PTCA, PCTA into proper zero-dependency libraries before interdependent-lib ships.

- [ ] PCEA: confirm zero-dep, fix `pcea/__init__.py` if still missing, fix import paths from `guardian_state.*` → `pcea.*`
- [ ] edcmbone: implement v2 per this proposal; ensure no imports outside stdlib
- [ ] ZFAE: implement (currently README/spec only); confirm zero-dep
- [ ] PCNA: confirm zero-dep
- [ ] PTCA: confirm zero-dep
- [ ] PCTA: confirm zero-dep
- [ ] interdependent-lib: wire all six as the only point of cross-dependency
- [ ] wayseer00/interdependent-lib: create as canonical individual mirror once aggregator is structurally complete

---

## 6) Provenance

This proposal was developed in conversation between Erin Spencer and Claude on 2026-05-01, building on prior threads (audit thread 2026-04-09, A0 identity thread 2026-04-07, repo consolidation thread 2026-04-06, frozen canon pack thread 2026-04-05, and earlier). The "lensing-as-structure" framing extends the polarity-balance principle from canon v1's bone inventory to the measurement architecture as a whole — a generalization the user explicitly chose ("option three, of course") over the more conservative alternatives of forcing the GPT module to conform to canon (option 1) or accepting flesh as a parallel substrate measuring the same metrics (option 2).

The substrate-to-embedder allocation (UCNS for bones, none for markers, ZFAE for flesh) was the structural insight that emerged once UCNS was identified as the canonical bone-domain embedding architecture. This allocation was not in prior memory and supersedes the earlier framing where ZFAE carried the entire embedding-dependent burden.

---

## 7) hmm-Tagged Items (Carried Forward, Not Yet Resolved)

Per canon convention, items marked `hmm:` are deferred decisions preserved as visible incompleteness rather than hidden assumption.

- **hmm:** Whether marker-domain C and flesh-domain C produce systematically related readings or are merely two independent operationalizations sharing a name — answerable empirically once both are computable on a test corpus
- **hmm:** Whether path (b)'s "Basin" can be defined without circular reference to its own metric (basin-as-attractor over trajectory of vectors that include basin-likeness)
- **hmm:** Whether `speech_act = quoted` requires a recursive Content reading on the quoted material (claim-within-claim)
- **hmm:** Whether the three-way Bridge requires a fourth coupling — A↔A across windows for each layer — for full temporal coverage, or whether trajectory metrics inside Behavioral cover this adequately
- **hmm:** Whether the Content layer's per-claim granularity collides with v1's per-turn / per-round granularity in a way that requires a new aggregation rule beyond simple averaging
