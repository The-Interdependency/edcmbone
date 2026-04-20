# CLAUDE.md — AI Assistant Guide for edcmbone

This file gives AI assistants (Claude Code and others) the context needed to work effectively in this repository.

---

## Project Overview

**edcmbone** is a pip-installable Python library and monorepo implementing the **EDCM-PCNA-PCTA Framework** (Extended Distributed Cognitive Model with PCNA/PCTA framework). Its primary function is measuring structural fidelity loss in AI interactions — quantifying how much meaning an AI system deletes when transforming structured user input. It consists of:

- A **Python backend** (`Backend/`) — core logic, transcript parsing, and canon data library
- A **React frontend** (`Frontend/`) — UI layer styled with Tailwind CSS
- An **AI Multimodel Hub** (`ammh/`) — sub-project for multi-model AI orchestration
- A **Tests** directory (`Tests/`) — test suite (currently being bootstrapped)
- A **Documentation** directory (`Documentation/`) — specs and design guidelines

**Current status**: Version 0.1.0. Four library modules are implemented and tested (87 tests, all passing). The frontend and AMMH server remain stubs.

---

## Current Use Case — GCIP Submission

edcmbone is now functioning as a civil rights evidence instrument in addition to its role as a research library. The **Global Cognitive Interaction Profiles (GCIP)** submission — a formal accessibility and safety complaint to Google, OpenAI, Anthropic, xAI, Meta, Microsoft, and regulatory bodies including the FTC, DOJ ADA Unit, EU AI Office, and the UN CRPD Committee — cites edcmbone as the measurement instrument for cognitive accessibility failures in AI systems. `Documentation/GCIP.md` contains the full proposal. `Documentation/evidence_log.md` contains three EDCM-measured evidence entries showing F-loss between 49.7% and 65.3%. `Documentation/neurodivergence_handling.md` is the source interaction rubric and AI skill specification underlying the proposal. The MIT license applies to all content; everything is open source.

---

## Repository Structure

```
edcmbone/
├── README.md                   # Library overview, quickstart, evidence log, failure taxonomy
├── Backend/
│   ├── pyproject.toml          # Python package config (Hatchling, src layout)
│   ├── requirements.txt        # Runtime dependencies (currently empty)
│   └── src/
│       └── edcmbone/
│           ├── __init__.py
│           ├── canon/
│           │   ├── __init__.py         # exports CanonLoader
│           │   ├── loader.py           # CanonLoader — bone/marker lookup API
│           │   └── data/
│           │       ├── bones_words_v1.json     # 253 free-word bones (PKQTS families)
│           │       ├── bones_affixes_v1.json   # 76 affix bones
│           │       ├── bones_punct_v1.json     # 13 punctuation bones
│           │       └── markers_v1.json         # 9-metric behavioral markers
│           ├── parser/
│           │   ├── __init__.py         # exports parse_transcript + data classes
│           │   └── turns_rounds.py     # Embedded-model transcript parser
│           ├── metrics/
│           │   ├── __init__.py         # exports all public symbols
│           │   ├── stats.py            # tokenise, TTR, entropy, novelty, cosine…
│           │   ├── risk.py             # four risk proxies (fixation/escalation/…)
│           │   ├── compute.py          # RoundMetrics, compute_round/transcript
│           │   ├── matrix.py           # A_MATRIX, PROJECTION_MAP, freeze/diff
│           │   └── projection.py       # AgentMetrics (CM,DA,DRIFT,DVG,INT,TBF), fire_alerts
│           └── compress.py             # Lossless codec + compression_stats
├── Frontend/
│   ├── package.json            # npm config (React 18.2.0 + Tailwind CSS)
│   └── tailwind.config.js      # Tailwind config (stub)
├── Tests/
│   └── test_backend.py         # Backend tests (stub)
├── ammh/
│   ├── README.md
│   └── backend/
│       └── server.py           # AMMH server (stub)
├── Documentation/
│   ├── README.md               # Documentation directory index
│   ├── spec.md                 # EDCM-PCNA-PCTA framework specification + math
│   ├── GCIP.md                 # Global Cognitive Interaction Profiles proposal
│   ├── evidence_log.md         # Three EDCM-measured evidence entries
│   ├── neurodivergence_handling.md  # Interaction rubric and AI skill specification
│   ├── auth_testing.md         # Authentication testing notes
│   └── design_guidelines.json  # Design guidelines
├── edcmbone_canon_data_v1.zip  # Source zip for canon data files (keep as reference)
├── .gitignore
├── LICENSE                     # MIT License, Copyright 2026
└── CLAUDE.md                   # This file
```

---

## Technology Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python >= 3.8, Hatchling packaging  |
| Frontend  | React 18.2.0, Tailwind CSS          |
| AMMH      | Python (server.py)                  |
| Tests     | pytest (not yet configured)         |
| Build     | Hatchling (Python), npm (Frontend)  |

---

## Development Workflows

### Backend (Python)

```bash
# Install in editable mode from the repo root (recommended)
pip install -e ./Backend

# Or from the Backend directory
cd Backend && pip install -e .

# Install test dependency
pip install -r Backend/requirements.txt
```

The Python package is named `edcmbone`. Full pipeline:

```python
from edcmbone.canon import CanonLoader
from edcmbone.parser import parse_transcript
from edcmbone.metrics import compute_transcript
import edcmbone.compress as codec

canon = CanonLoader()

# 1. Parse transcript -> turns, rounds, bone/flesh tokens
pt = parse_transcript(transcript, canon=canon)

# 2. Compute 11-component metric vector per round
metrics = compute_transcript(pt, canon=canon)
# -> [RoundMetrics(C, R, F, E, D, N, I, O, L, P, kappa), ...]

# 3. Lossless encode + compress
compressed = codec.to_bytes(pt, metrics)
pt2, metrics2 = codec.from_bytes(compressed)   # exact reconstruction

# 4. Compression-metric statistics
stats = codec.compression_stats(transcript, compressed, pt)
# -> {structural_density, bone_entropy_bits, huffman_codes, ...}
```

### Frontend (React)

```bash
cd Frontend
npm install
npm start      # dev server
npm run build  # production build
```

Tailwind CSS is included; configure `tailwind.config.js` with `content` paths before using utility classes.

### Running Tests

```bash
# From repo root
pytest Tests/

# Or from Backend/ (pytest.ini_options points to ../Tests)
cd Backend && pytest
```

87 tests covering canon, parser, metrics, compress, projection, and matrix. All pass. pytest >= 7.0 is the only test dependency (listed in `requirements.txt`).

---

## Key Conventions

### Python
- Package lives under `Backend/src/edcmbone/` — standard `src/` layout configured via `[tool.hatch.build] sources = ["src"]`
- Python 3.8+ compatible code required (no 3.9+ syntax like `list[int]` type hints without `from __future__ import annotations`)
- `pyproject.toml` is the source of truth for metadata; `requirements.txt` is for direct runtime deps
- JSON data files bundled with the package must be listed in `[tool.hatch.build.targets.wheel] include`
- No linter configured yet — when adding one, prefer `ruff` for linting/formatting

### JavaScript / React
- React 18.2.0, functional components and hooks (no class components)
- Tailwind CSS for styling — no inline styles or CSS modules unless there's a specific reason
- No TypeScript configured — use plain JS unless the project explicitly migrates
- No ESLint configured yet — when adding one, prefer `eslint` with `eslint-plugin-react`

### General
- Keep stub/placeholder files until they are implemented; do not delete them prematurely
- Documentation lives in `Documentation/` — update `spec.md` and `README.md` as the domain model evolves
- MIT License; all new files should be consistent with open-source expectations

---

## Domain Model — Key Concepts

Read `Documentation/spec.md` for the full framework specification. Short orientation:

- **Bones**: operator tokens that carry structural constraint weight, classified into PKQTS families (Polarity, Quantification, Qualification, Topology, Structuring)
- **Flesh**: tokens that modulate magnitude only — excluded from bone inventory
- **Markers**: phrase-level signals for the 9 behavioral metrics (C, R, D, N, L, O, F, E, I)
- **Metrics**: the 9-component vector **M**_t measuring system state per round; see spec.md §3 for the full formulation
- **Rounds vs Turns**: rounds are the unit of metric computation; turns are speaker utterances within a round

The canon data files in `Backend/src/edcmbone/canon/data/` are the authoritative inventory. Do not edit them manually — they are versioned (`_v1`) and will be superseded by new versions.

---

## Important Files to Know

| File | Purpose |
|------|---------|
| `README.md` | Library overview, quickstart, evidence log, failure taxonomy |
| `Backend/pyproject.toml` | Python package metadata, build system, data-file inclusion |
| `Backend/src/edcmbone/canon/loader.py` | `CanonLoader` — bone/marker lookup API |
| `Backend/src/edcmbone/canon/data/*.json` | Authoritative canon data (bones + markers) |
| `Backend/src/edcmbone/parser/turns_rounds.py` | Embedded-model transcript parser |
| `Backend/src/edcmbone/metrics/stats.py` | Text statistics (TTR, entropy, cosine, …) |
| `Backend/src/edcmbone/metrics/risk.py` | Four risk proxies |
| `Backend/src/edcmbone/metrics/compute.py` | Metric vector + RC-circuit energy |
| `Backend/src/edcmbone/metrics/matrix.py` | A_MATRIX, PROJECTION_MAP, ALERT_THRESHOLDS, freeze/diff |
| `Backend/src/edcmbone/metrics/projection.py` | AgentMetrics (CM, DA, DRIFT, DVG, INT, TBF), fire_alerts |
| `Backend/src/edcmbone/compress.py` | Lossless codec + Huffman compression stats |
| `Tests/test_backend.py` | 87-test suite (canon, parser, metrics, compress, projection, matrix) |
| `Frontend/package.json` | Frontend dependencies and scripts |
| `ammh/backend/server.py` | AMMH multi-model hub server (stub) |
| `Documentation/spec.md` | Full framework specification including mathematics |
| `Documentation/GCIP.md` | Global Cognitive Interaction Profiles proposal |
| `Documentation/evidence_log.md` | Three EDCM-measured evidence entries |
| `Documentation/neurodivergence_handling.md` | Interaction rubric and AI skill specification |

---

## What Does Not Exist Yet (Do Not Assume)

- No CI/CD pipeline (no `.github/workflows/`)
- No environment variable file (`.env` or `.env.example`)
- No linting or formatting configs (`pyproject.toml [tool.ruff]`, `.eslintrc`, `.prettierrc`)
- No pre-commit hooks
- `Backend/requirements.txt` has `pytest>=7.0` — add further runtime deps as introduced
- pytest IS configured: `[tool.pytest.ini_options]` in `Backend/pyproject.toml` sets `testpaths = ["../Tests"]`
- `tailwind.config.js` is empty — add `content` globs before using Tailwind classes
- `ammh/backend/server.py` is a stub — no routes implemented

When implementing any of the above, use the most current conventions for the respective toolchain.

---

## Git Workflow

- Main branch: `master`
- Feature branches follow the pattern: `<type>/<description>-<id>` (e.g., `claude/add-claude-documentation-hl6si`)
- Commit messages should be clear and descriptive
- Author: Erin Patrick Spencer (erin.eps.hovel@gmail.com)
