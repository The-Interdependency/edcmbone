# CLAUDE.md — AI Assistant Guide for edcmbone

This file gives AI assistants (Claude Code and others) the context needed to work effectively in this repository.

---

<!-- BEGIN GENERATED:manifest -->
<!-- Generated from pyproject + repo tree by .agents/skills/manifest/generate.py — DO NOT EDIT BY HAND. Refresh with `python .agents/skills/manifest/generate.py --pyproject backend/pyproject.toml --write`. -->

| Field | Value |
|---|---|
| Package | `edcmbone-backend` |
| Version | `0.2.0` |
| Description | MSDMD-compliant UCNS-only backend for EDCM boundary objects |
| Status | hmmm |
| Python | >=3.8 |
| License | MPL-2.0 |
| Build backend | `hatchling.build` |
| Author(s) | hmmm |
| Repository | hmmm |
| Runtime dependencies | none (stdlib only) |
| Optional extras | none |
| Keywords | none |
| CI workflows | `ci.yml`, `manifest-check.yml` |
| Top-level directories | `aimmh-lib/` · `backend/` · `backend_old/` · `canon_eng/` · `core/` · `docs/` · `edcmbone/` · `frontend/` · `tests/` |

<sub>Derived from `backend/pyproject.toml` + the repo tree. Unknown fields surface as `hmmm` rather than a guess.</sub>
<!-- END GENERATED:manifest -->

> Generated from `backend/pyproject.toml` (the canonical installable package) +
> the repo tree, gated by `.github/workflows/manifest-check.yml`. These are the
> **as-packaged** facts; the "Status" note below explains the known
> version inconsistency (`version.py` says `1.0.1` while the package declares
> `0.1.0`). The license is now MPL-2.0 consistently across root `LICENSE`,
> `backend/LICENSE`, and `backend/pyproject.toml`. Refresh with
> `python .agents/skills/manifest/generate.py --pyproject backend/pyproject.toml --write`.

## Project Overview

**edcmbone** is a pip-installable Python library and monorepo implementing the **EDCM-PCNA-PCTA Framework** (Energy–Dissonance Circuit Model with Prime Circle Neural Architecture + Prime Circled Tensor Architecture). Its primary function is measuring structural fidelity loss in AI interactions — quantifying how much meaning an AI system deletes when transforming structured user input.

> **Cross-reference — prime-tensor stack canon.** The canonical meaning and boundaries of the `PCNA` term (layer 1, **Prime Circle Neural Architecture**: tensors → circles in a back-propagating NN → weights) and the `PCTA` term (layer 2, **Prime Circled Tensor Architecture**: circles → seeds) live in `The-Interdependency/interdependent-lib : docs/prime-tensor-stack.md` — since the 2026-07 consolidation those layers are the `neural`/`circle` and `seed` modules of the single **`ptcna`** package (`The-Interdependency/ptcna`; the former standalone `pcna`/`pcta`/`pcsa` repos are superseded) — that role-and-boundary map is the source of truth, not this repo. The acronym expansions, the per-layer flow, and the variable-count rule (composition counts are variable; the only invariant is that every circle/seed/core is itself a tensor) were resolved by the maintainer on 2026-06-05. edcmbone is a measurement instrument that merely *names* these framework terms; consuming or naming PCNA / PCTA here transfers **none** of their (or UCNS-A's) theorem / proof / empirical status to EDCM, edcmbone, or UCNS-G (consistent with the UCNS-boundary non-transfer rule in `docs/ucns-boundary.md`).

**Status**: The repo-wide constant in `version.py` is `1.0.1`; the installable package (`backend/pyproject.toml`) declares `0.1.0` (Development Status: 3 - Alpha). The canonical, tested package lives under `backend/src/edcmbone/` and ships four working module groups (canon, parser, metrics, compress) plus `ucns/`. A root-level `edcmbone/` package and a `core/` framework package are an in-progress layer migration — mostly stubs or partial (see below).

The project also functions as a civil-rights evidence instrument in the **Global Cognitive Interaction Profiles (GCIP)** submission — a formal accessibility and safety complaint to major AI labs and regulatory bodies. `canon_eng/GCIP.md` contains the full proposal.

**License**: **MPL-2.0** (Mozilla Public License 2.0 — weak, file-level copyleft: embed anywhere, but changes to these files must be published) — consistent across the root `LICENSE`, the package-bundled `backend/LICENSE`, and `backend/pyproject.toml` (`license = { text = "MPL-2.0" }` with the MPL-2.0 classifier). Relicensed from MIT (which had itself superseded the earlier AGPL-intent / Apache-as-packaged inconsistency and the former commercial dual-license). Copyright (c) 2026 Erin Patrick Spencer.

---

## Repository Structure

```
edcmbone/
├── README.md                        # Library overview, evidence log, quickstart, GCIP
├── CLAUDE.md                        # This file
├── LICENSE                          # MPL-2.0
├── .gitignore
├── __init__.py                      # Empty package marker (0 lines; no import side effects)
├── version.py                       # __version__ = "1.0.1" (repo-wide constant)
├── pytest.ini                       # testpaths = tests
│
├── backend/                         # CANONICAL pip package (src layout, tested)
│   ├── pyproject.toml               # name=edcmbone, version=0.1.0, Hatchling; declares license = MPL-2.0
│   ├── README.md                    # PyPI long description (keep in sync with root README)
│   ├── LICENSE                      # MPL-2.0 license text bundled with package
│   └── src/edcmbone/
│       ├── __init__.py              # __version__ = "0.1.0"; re-exports public API
│       ├── canon/
│       │   ├── loader.py            # CanonLoader — bone/marker lookup API
│       │   └── data/
│       │       ├── bones_words_v1.json    # free-word bones (PKQTS families)
│       │       ├── bones_affixes_v1.json  # affix bones
│       │       ├── bones_punct_v1.json    # punctuation bones
│       │       └── markers_v1.json        # 9-metric behavioral markers (C,R,D,N,...)
│       ├── parser/turns_rounds.py   # Embedded-model transcript parser
│       ├── metrics/
│       │   ├── stats.py             # tokenize, TTR, entropy, novelty, cosine
│       │   ├── risk.py              # risk proxies (fixation, escalation, ...)
│       │   ├── compute.py           # RoundMetrics, compute_round/transcript
│       │   ├── matrix.py            # A_MATRIX, PROJECTION_MAP, freeze/diff
│       │   ├── projection.py        # AgentMetrics (CM,DA,DRIFT,DVG,INT,TBF)
│       │   └── orthogonality.py     # metric orthogonality (v0.2)
│       ├── ucns/                    # local closed-token / marker encoding layer
│       │   ├── ucns_v04.py
│       │   └── closed_tokens.py
│       └── compress.py              # Lossless zlib codec + compression stats
│
├── edcmbone/                        # Root-level refactor target (IN PROGRESS — mostly stubs)
│   ├── __init__.py                  # `from version import __version__`
│   ├── config.py / engine.py / errors.py / types.py   # EMPTY stubs (0 lines)
│   ├── behavioral/ bridge/ cli/ ingest/ operator/      # scaffolded
│   ├── parse/ routing/ (pcna/, pcta/)                  # scaffolded
│   ├── ucns_g/                      # UCNS-G v3 prime-cylinder schema (substantive)
│   └── edcmbone/                    # nested duplicate scaffold
│
├── core/                            # Core framework package (IN PROGRESS — partial)
│   ├── parsing/ operator/          # substantive implementations
│   ├── bridge/ (bridge_engine.py)  # substantive; divergence/correlation stubs
│   ├── behavioral/ pcna/ windowing/
│
├── canon_eng/                       # Frozen structural canon (specs + JSON schemas)
│   ├── spec.md GCIP.md edcm.md parser.md function.md dataflow.md ...
│   ├── *_schema_v1.json             # actor/turn/round/operator/bridge/utterance schemas
│   └── release/                     # v1.0.0 release + freeze statements
│
├── docs/                            # Working docs, specs, handoffs
│   ├── spec.md ucns-boundary.md ingest.md routing.md ...
│   ├── specs/edcm-ucns-metric-orthogonality-v0.2.md
│   └── handoffs/2026-05-22-ucns-g-prime-cylinder-v3.md
│
├── aimmh-lib/backend/server.py      # AI Multimodel Hub server (stub)
├── frontend/                        # package.json (react ^18.2.0), tailwind, src/ucns_g/types.ts
│
├── tests/                           # pytest suite — currently passing (see "Build / Test")
│   ├── test_*.py (11 modules)        # NOTE: test_backend.py is empty; coverage lives in the others
│   ├── run_all.py                   # standalone validation harness (uses root engine.py)
│   ├── conftest.py                  # sys.path shim: backend/src ahead of repo root
│   ├── fixtures/ golden/
│
├── engine.py                        # Top-level v1.0.0 engine (consumed by tests/run_all.py)
├── closed_tokens.py                 # Root closed-token table (L0 reference)
├── ucns_v04.py                      # Root UCNS v0.4 reference
├── *_probe.py                       # Research probes (phi_compose, frequency, widening, ...)
├── AUDIT_REGRADE.md                 # Layer re-grading findings
├── LAYER_MIGRATION_PLAN.md          # edcmbone → future `edcm` package contract
└── edcmbone_canon_data_v1.zip       # Source zip for canon data (reference only)
```

> Note: there are no capitalized `Backend/`, `Frontend/`, `Documentation/`, or `Tests/` directories. Only the lowercase variants exist.

---

## Which Package to Use

| Layout | Path | Status | When to Use |
|--------|------|--------|-------------|
| **Canonical** | `backend/src/edcmbone/` | `tests/` suite passing (≈78 tests at time of writing) | Installing and consuming the library |
| **Refactor target** | `edcmbone/` (root) + `core/` | In-progress migration; many empty/partial files | Adding new architecture — fill stubs here |

The repo root and `backend/src` both contain an `edcmbone` package. `tests/conftest.py` puts `backend/src` ahead of the repo root on `sys.path` so the canonical package shadows the incomplete root one. Do not assume root `edcmbone/` files are implemented — `engine.py`, `types.py`, `config.py`, `errors.py` there are empty.

---

## Technology Stack

| Layer     | Technology                                   |
|-----------|----------------------------------------------|
| Backend   | Python >= 3.8, Hatchling packaging, no runtime deps |
| Frontend  | React ^18.2.0, Tailwind CSS (minimal scaffold) |
| AIMMH-LIB | Python (`server.py` stub)                    |
| Tests     | pytest (CI installs latest); `jsonschema` optional |
| CI        | GitHub Actions — `.github/workflows/ci.yml`  |

---

## Build / Test / Run (verified)

### Install

```bash
pip install -e ./backend          # editable install of the canonical package
```

No `requirements.txt` exists; the package declares zero runtime dependencies. Install `pytest` separately for tests (`jsonschema` is optional and only enables schema checks).

### Test

```bash
pytest                            # uses pytest.ini -> testpaths=tests; suite passes (~78 tests, spread across tests/test_*.py — test_backend.py is currently empty)
python tests/run_all.py           # standalone harness: smoke transcript + golden compare
```

CI (`.github/workflows/ci.yml`) runs on push to `main` and on PRs: Python 3.11, `pip install pytest`, `pip install -e ./backend`, then `pytest`.

> Gotcha: `backend/pyproject.toml` has a stale `[tool.pytest.ini_options] testpaths = ["../Tests", "../tests"]` pointing at a non-existent `../Tests`. The repo-root `pytest.ini` (`testpaths = tests`) is what actually governs `pytest` runs from the repo root.

### Lint

No linter is configured (no ruff/flake8/black config present). Prefer `ruff` if adding one.

### Run (library usage)

```python
from edcmbone.canon import CanonLoader
from edcmbone.parser import parse_transcript
from edcmbone.metrics import compute_transcript
import edcmbone.compress as codec

canon = CanonLoader()
pt = parse_transcript(transcript, canon=canon)
metrics = compute_transcript(pt, canon=canon)
compressed = codec.to_bytes(pt, metrics)
stats = codec.compression_stats(transcript, compressed, pt)   # stats['structural_density'] == F
```

### Frontend

`frontend/` is a minimal scaffold (a `package.json` with only `react` and a Tailwind config). There are no build/start scripts defined — do not assume `npm start`/`npm run build` work until scripts are added.

---

## Domain Model — Key Concepts

- **Bones**: operator tokens carrying structural constraint weight — classified into **PKQTS** families (Polarity, Quantification, Qualification, Topology, Structuring).
- **Flesh**: tokens that modulate magnitude only — excluded from the bone inventory.
- **Markers**: phrase-level signals for the behavioral metrics (`markers_v1.json` keys include C, R, D, N, ...).
- **Rounds vs Turns**: rounds are the unit of metric computation; turns are speaker utterances within a round.
- **Layer stack** (per `LAYER_MIGRATION_PLAN.md`): **L0** bones-only operator layer (edcmbone is canonical L0); **L1** Arc Style `M_t = A·φ`; **L2** risk composites; **L3** projection (CM, DA, DRIFT, DVG, INT, TBF); **Bridge** is observational-only correlation, orthogonal to the stack. The future upstream `edcm` package (not yet created) is intended to consume edcmbone (L0) + `ucns` and produce L1/L2/L3.
- **F (F-loss)**: structural fidelity / operator density, computed as `structural_density` in `compress.compression_stats()`. F-loss ≥ 20% = degradation; ≥ 50% = significant failure; structural density rising with F-loss = decorative preservation (F6).
- **Failure taxonomy**: F1 Deletion, F2 Mutation, F3 Inversion, F4 Category Collapse, F5 Persistence Failure, F6 Decorative Preservation.

### UCNS boundary (important)

These are distinct objects in distinct repos — not synonyms (see `docs/ucns-boundary.md`):

- **`edcmbone.ucns`** (this repo): local closed-token / marker encoding layer (`backend/src/edcmbone/ucns/`, root `closed_tokens.py`).
- **UCNS-A** (`The-Interdependency/ucns`): recursive factorization algebra.
- **UCNS-G**: EDCM metric geometry — prime-indexed Möbius-cylinder metric disks (`edcmbone/ucns_g/`, `docs/handoffs/2026-05-22-ucns-g-prime-cylinder-v3.md`).

**No UCNS-A theorem/proof status transfers to EDCM, edcmbone, or UCNS-G** unless an explicit source-backed bridge is added.

---

## Conventions & Gotchas

- **Canonical code is `backend/src/edcmbone/`** — standard `src/` layout. Root `edcmbone/` and `core/` are migration targets; check for empty/stub files before relying on them.
- Python 3.8+ compatible: use `from __future__ import annotations` rather than 3.9+ syntax.
- `backend/pyproject.toml` is the source of truth for package metadata; there is no `requirements.txt`.
- JSON canon data under `backend/src/edcmbone/canon/data/` is versioned (`_v1`) — **do not edit manually**; it is generated/frozen (source: `edcmbone_canon_data_v1.zip`).
- `backend/README.md` mirrors the root `README.md` for PyPI — keep in sync.
- `canon_eng/` holds the **frozen structural canon** (specs + `*_schema_v1.json`). Code must consume canon, not "improve" it (see header comments in `engine.py`).
- `tests/conftest.py` performs deliberate `sys.path` ordering — do not reorder it; it keeps the canonical `edcmbone` package ahead of the incomplete root one.
- Repository skills: `.agents/skills/README.md` notes agents should read `meta-module-build/SKILL.md` before scaffolding new modules, schemas, engines, etc.
- "hmmm:" inline comments mark open constraints / intent notes throughout the canon and engine; respect them as guardrails.

### Known stale/quirky items

- `backend/pyproject.toml` testpaths reference a non-existent `../Tests` (use repo-root `pytest.ini` instead).
- `version.py` (1.0.1) and `backend/pyproject.toml` (0.1.0) disagree — expected during the migration.

---

## Git Workflow

- Main branch: `main`.
- Feature branches: `feat/…`, `fix/…`, `docs/…`, `chore/…` (e.g. `claude/<topic>-<id>`).
- Commit style: Conventional Commits (`feat(metrics):`, `fix(canon):`, `docs:`…).
- Author: Erin Patrick Spencer (wayseer@interdependentway.org).
- License: MPL-2.0 (weak copyleft — embed anywhere, but changes to these files must be published; relicensed from MIT).

---

## Key Files Quick Reference

| File | Purpose |
|------|---------|
| `backend/pyproject.toml` | Package metadata and build config |
| `backend/src/edcmbone/canon/loader.py` | `CanonLoader` — bone/marker lookup |
| `backend/src/edcmbone/canon/data/*.json` | Authoritative canon data (do not edit) |
| `backend/src/edcmbone/parser/turns_rounds.py` | Transcript parser |
| `backend/src/edcmbone/metrics/compute.py` | Metric vector computation |
| `backend/src/edcmbone/metrics/projection.py` | AgentMetrics + alert firing |
| `backend/src/edcmbone/compress.py` | Lossless codec + compression stats (F) |
| `tests/test_*.py` | Test suite (11 modules; coverage in `test_smoke.py`, `test_metric_orthogonality_v02.py`, `test_ucns_objects.py`, `test_closed_tokens.py`, etc. — `test_backend.py` is currently empty) |
| `tests/run_all.py` | Standalone validation harness (root `engine.py`) |
| `canon_eng/spec.md` | Full framework specification |
| `canon_eng/GCIP.md` | Global Cognitive Interaction Profiles proposal |
| `docs/ucns-boundary.md` | UCNS-A / UCNS-G / `edcmbone.ucns` boundary discipline |
| `LAYER_MIGRATION_PLAN.md` | edcmbone → future `edcm` package contract |
| `engine.py` (root) | v1.0.0 engine consumed by `tests/run_all.py` |

---

edcmbone · MPL-2.0 · [The Interdependent Way](https://github.com/The-Interdependency)
Contact: [wayseer@interdependentway.org](mailto:wayseer@interdependentway.org)
