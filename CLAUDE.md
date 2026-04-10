# CLAUDE.md — AI Assistant Guide for edcmbone

This file gives AI assistants (Claude Code and others) the context needed to work effectively in this repository.

---

## Project Overview

**edcmbone** is an early-stage monorepo implementing the **EDCM-PCNA-PCTA Framework** (Extended Distributed Cognitive Model with PCNA/PCTA framework). It consists of:

- A **Python backend** (`Backend/`) — core logic, transcript parsing, and canon data library
- A **React frontend** (`Frontend/`) — UI layer styled with Tailwind CSS
- An **AI Multimodel Hub** (`ammh/`) — sub-project for multi-model AI orchestration
- A **Tests** directory (`Tests/`) — test suite (currently being bootstrapped)
- A **Documentation** directory (`Documentation/`) — specs and design guidelines

**Current status**: Version 0.1.0. The canon data library (`edcmbone.canon`) is implemented. Other source files remain stubs. Active implementation is in progress.

---

## Repository Structure

```
edcmbone/
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
│           └── parser/
│               └── turns_rounds.py     # Transcript parser (stub)
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
│   ├── README.md               # Project README
│   ├── spec.md                 # EDCM-PCNA-PCTA framework specification + math
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
# Install in editable mode from the Backend directory
cd Backend
pip install -e .

# Or install requirements directly
pip install -r requirements.txt
```

The Python package is named `edcmbone`. Primary entry points:

```python
# Canon data library (implemented)
from edcmbone.canon import CanonLoader

canon = CanonLoader()
canon.lookup_word("not")           # -> {"word": "not", "primary": "P", "families": ["P"], ...}
canon.lookup_affix("un-")          # -> {"affix": "un-", "primary": "P", ...}
canon.lookup_punct("?")            # -> {"mark": "?", "primary": "Q", "tokens_emitted": 1, ...}
canon.metric_names()               # -> ["C", "R", "D", "N", "L", "O", "F", "E", "I"]
canon.metric_info("R")             # -> {metric, formula, computable_from_markers, markers, ...}
canon.marker_phrases("R", "refusal")  # -> ["I can't", "I won't", ...]

# Transcript parser (stub)
from edcmbone.parser.turns_rounds import parse_transcript
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
# From repo root or Tests/
pytest Tests/
```

No pytest configuration exists yet. When adding tests, use `pytest` with standard conventions (`test_*.py` files, `test_*` functions).

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
| `Backend/pyproject.toml` | Python package metadata, build system, data-file inclusion |
| `Backend/src/edcmbone/canon/loader.py` | `CanonLoader` — primary implemented API |
| `Backend/src/edcmbone/canon/data/*.json` | Authoritative canon data (bones + markers) |
| `Backend/src/edcmbone/parser/turns_rounds.py` | Transcript parser (stub, next to implement) |
| `Frontend/package.json` | Frontend dependencies and scripts |
| `ammh/backend/server.py` | AMMH multi-model hub server (stub) |
| `Documentation/spec.md` | Canonical framework specification including mathematics |
| `Tests/test_backend.py` | Backend test entry point (stub) |

---

## What Does Not Exist Yet (Do Not Assume)

- No CI/CD pipeline (no `.github/workflows/`)
- No environment variable file (`.env` or `.env.example`)
- No linting or formatting configs (`pyproject.toml [tool.ruff]`, `.eslintrc`, `.prettierrc`)
- No pre-commit hooks
- No pytest configuration (`pytest.ini` or `[tool.pytest.ini_options]`)
- `requirements.txt` is empty — add dependencies as they are introduced
- `tailwind.config.js` is empty — add `content` globs before using Tailwind classes
- `parser/turns_rounds.py` is a stub — `parse_transcript` returns `None`
- `ammh/backend/server.py` is a stub — no routes implemented

When implementing any of the above, use the most current conventions for the respective toolchain.

---

## Git Workflow

- Main branch: `master`
- Feature branches follow the pattern: `<type>/<description>-<id>` (e.g., `claude/add-claude-documentation-hl6si`)
- Commit messages should be clear and descriptive
- Author: Erin Patrick Spencer (erin.eps.hovel@gmail.com)
