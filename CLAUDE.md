# CLAUDE.md — AI Assistant Guide for edcmbone

This file gives AI assistants (Claude Code and others) the context needed to work effectively in this repository.

---

## Project Overview

**edcmbone** is a pip-installable Python library and monorepo implementing the **EDCM-PCNA-PCTA Framework** (Extended Distributed Cognitive Model with PCNA/PCTA framework). Its primary function is measuring structural fidelity loss in AI interactions — quantifying how much meaning an AI system deletes when transforming structured user input.

**Current status**: Version 0.1.0. The library ships four tested modules (canon, parser, metrics, compress). The repo also carries a newer in-progress package refactoring (`edcmbone/` root-level) and a `core/` framework package — both are partially scaffolded (see below).

The project also functions as a civil rights evidence instrument in the **Global Cognitive Interaction Profiles (GCIP)** submission — a formal accessibility and safety complaint to major AI labs and regulatory bodies. `Documentation/GCIP.md` contains the full proposal.

---

## Repository Structure

```
edcmbone/
├── README.md
├── CLAUDE.md                        # This file
├── LICENSE                          # MIT License
├── .gitignore
├── __init__.py                      # Root package marker
├── version.py                       # Version stub
│
├── Backend/                         # Original pip package (stable, tested)
│   ├── pyproject.toml               # Package config (Hatchling, src layout)
│   ├── README.md                    # PyPI long description (keep in sync with root README)
│   ├── requirements.txt             # Dev/test deps (pytest>=7.0)
│   └── src/
│       └── edcmbone/
│           ├── __init__.py
│           ├── canon/
│           │   ├── loader.py        # CanonLoader — bone/marker lookup API
│           │   └── data/
│           │       ├── bones_words_v1.json    # 253 free-word bones (PKQTS families)
│           │       ├── bones_affixes_v1.json  # 79 affix bones
│           │       ├── bones_punct_v1.json    # 13 punctuation bones
│           │       └── markers_v1.json        # 9-metric behavioral markers
│           ├── parser/
│           │   └── turns_rounds.py  # Embedded-model transcript parser
│           ├── metrics/
│           │   ├── stats.py         # tokenise, TTR, entropy, novelty, cosine
│           │   ├── risk.py          # four risk proxies
│           │   ├── compute.py       # RoundMetrics, compute_round/transcript
│           │   ├── matrix.py        # A_MATRIX, PROJECTION_MAP, freeze/diff
│           │   └── projection.py    # AgentMetrics (CM,DA,DRIFT,DVG,INT,TBF), fire_alerts
│           └── compress.py          # Lossless codec + Huffman compression stats
│
├── backend/                         # Lowercase alias / restructured package layout
│   ├── pyproject.toml
│   ├── README.md
│   ├── requirements.txt
│   └── src/                         # Mirror of Backend/src — evolving
│
├── edcmbone/                        # Root-level refactored package (IN PROGRESS — stubs)
│   ├── __init__.py
│   ├── config.py                    # stub
│   ├── engine.py                    # stub
│   ├── errors.py                    # stub
│   ├── types.py                     # stub
│   ├── behavioral/                  # behavioral metrics module (scaffolded)
│   ├── bridge/                      # bridge layer (scaffolded)
│   ├── canon/                       # canon loader (scaffolded)
│   ├── cli/                         # CLI interface (scaffolded)
│   ├── edcmbone/                    # nested edcmbone package (scaffolded)
│   ├── ingest/                      # transcript ingestion (scaffolded)
│   ├── operator/                    # operator logic (scaffolded)
│   ├── parse/                       # parser refactor (scaffolded)
│   └── routing/                     # routing layer (scaffolded)
│
├── core/                            # Core framework package (IN PROGRESS — partially implemented)
│   ├── __init__.py
│   ├── behavioral/
│   ├── bridge/
│   ├── operator/
│   ├── parsing/
│   ├── pcna/
│   └── windowing/
│
├── canon_eng/                       # Canon engine utilities
├── aimmh-lib/
│   └── backend/server.py            # AIMMH-LIB multi-model hub server (stub)
├── Frontend/
│   ├── package.json                 # React 18.2.0 + Tailwind CSS
│   └── tailwind.config.js
├── frontend/                        # Lowercase alias / evolving frontend
│
├── Documentation/
│   ├── spec.md                      # Full framework specification
│   ├── GCIP.md                      # Global Cognitive Interaction Profiles proposal
│   ├── evidence_log.md              # Three EDCM-measured evidence entries
│   └── neurodivergence_handling.md  # Interaction rubric and AI skill specification
├── docs/                            # Additional docs (evolving)
│
├── Tests/                           # Original test suite
│   └── test_backend.py              # 87-test suite (all pass)
├── tests/                           # Lowercase alias / new test location
│
├── engine.py                        # Top-level engine entry point
├── closed_tokens.py                 # Closed-token vocabulary
├── ucns_v04.py                      # UCNS v0.4 reference implementation
└── edcmbone_canon_data_v1.zip       # Source zip for canon data files (reference only)
```

---

## Dual Package Layout — What to Use

The repo currently has **two parallel package structures**:

| Layout | Path | Status | When to Use |
|--------|------|--------|-------------|
| **Stable** | `Backend/src/edcmbone/` | 87 tests passing, production-ready | Installing and consuming the library |
| **Refactor** | `edcmbone/` (root) and `core/` | Partially implemented refactor-in-progress; see individual module docstrings for what is and isn't complete | Adding new architecture — fill in stubs here |

Do not assume all files in `edcmbone/` (root) or `core/` contain working implementations. `core/parsing/`, `core/operator/`, and `core/bridge/` now contain substantive implementations; other subdirectories may still be stubs. The **stable** code lives under `Backend/src/edcmbone/`.

---

## Technology Stack

| Layer     | Technology                          |
|-----------|-------------------------------------|
| Backend   | Python >= 3.8, Hatchling packaging  |
| Frontend  | React 18.2.0, Tailwind CSS          |
| AIMMH-LIB | Python (server.py stub)             |
| Tests     | pytest >= 7.0                       |
| Build     | Hatchling (Python), npm (Frontend)  |

---

## Development Workflows

### Backend (Python — stable path)

```bash
# Install from Backend/ (stable, tested)
pip install -e ./Backend
pip install -r Backend/requirements.txt

# Run tests
pytest Tests/
# or from Backend/:
cd Backend && pytest
```

### Backend (Python — refactor path)

```bash
# Install from backend/ (lowercase — evolving)
pip install -e ./backend
```

### Full pipeline (stable)

```python
from edcmbone.canon import CanonLoader
from edcmbone.parser import parse_transcript
from edcmbone.metrics import compute_transcript
import edcmbone.compress as codec

canon = CanonLoader()
pt = parse_transcript(transcript, canon=canon)
metrics = compute_transcript(pt, canon=canon)
compressed = codec.to_bytes(pt, metrics)
stats = codec.compression_stats(transcript, compressed, pt)
```

### Frontend (React)

```bash
cd Frontend
npm install
npm start
npm run build
```

---

## Key Conventions

### Python
- Stable package lives under `Backend/src/edcmbone/` — standard `src/` layout
- Python 3.8+ compatible (no 3.9+ syntax without `from __future__ import annotations`)
- `pyproject.toml` is source of truth for metadata; `requirements.txt` for dev/test deps
- JSON canon data files under `src/edcmbone/canon/data/` are versioned (`_v1`) — do not edit manually
- `Backend/README.md` mirrors root `README.md` for PyPI — keep in sync
- When filling in stubs in `edcmbone/` (root): follow the same conventions as `Backend/src/edcmbone/`

### JavaScript / React
- React 18.2.0, functional components and hooks
- Tailwind CSS for styling
- No TypeScript, no ESLint configured yet

### General
- MIT License; all new files consistent with open-source expectations
- `Documentation/` is the authoritative docs directory; `docs/` is supplementary

---

## Domain Model — Key Concepts

- **Bones**: operator tokens carrying structural constraint weight — classified into PKQTS families (Polarity, Quantification, Qualification, Topology, Structuring)
- **Flesh**: tokens that modulate magnitude only — excluded from bone inventory
- **Markers**: phrase-level signals for the 9 behavioral metrics (C, R, D, N, L, O, F, E, I)
- **Rounds vs Turns**: rounds are the unit of metric computation; turns are speaker utterances within a round
- **F-loss**: structural fidelity loss metric — quantifies meaning deletion by an AI system

---

## Important Files

| File | Purpose |
|------|---------|
| `README.md` | Library overview, quickstart, evidence log |
| `Backend/pyproject.toml` | Python package metadata and build config |
| `Backend/src/edcmbone/canon/loader.py` | `CanonLoader` — bone/marker lookup API |
| `Backend/src/edcmbone/canon/data/*.json` | Authoritative canon data (do not edit) |
| `Backend/src/edcmbone/parser/turns_rounds.py` | Transcript parser |
| `Backend/src/edcmbone/metrics/compute.py` | Metric vector computation |
| `Backend/src/edcmbone/metrics/projection.py` | AgentMetrics and alert firing |
| `Backend/src/edcmbone/compress.py` | Lossless codec + compression stats |
| `Tests/test_backend.py` | 87-test suite (canon, parser, metrics, compress) |
| `Documentation/spec.md` | Full framework specification with mathematics |
| `Documentation/GCIP.md` | Global Cognitive Interaction Profiles proposal |
| `closed_tokens.py` | Closed-token vocabulary (top-level) |
| `ucns_v04.py` | UCNS v0.4 reference (top-level) |
| `engine.py` | Top-level engine entry point |

---

## What Does Not Exist Yet

- No CI/CD pipeline
- No linting configs (prefer `ruff` when adding)
- No pre-commit hooks
- `edcmbone/` (root) stubs — not yet fully implemented (see individual module docstrings)
- `core/` — partially implemented refactor-in-progress; `core/parsing/`, `core/operator/`, and `core/bridge/` contain substantive implementations; other subdirectories may still be stubs
- `aimmh-lib/backend/server.py` is a stub
- `tailwind.config.js` needs `content` globs before use
- Frontend tests

---

## Git Workflow

- Main branch: `master`
- Feature branches: `<type>/<description>-<id>` (e.g., `claude/add-feature-abc123`)
- Author: Erin Patrick Spencer (erin.eps.hovel@gmail.com)
- License: MIT
