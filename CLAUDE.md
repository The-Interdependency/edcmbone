# CLAUDE.md — AI Assistant Guide for edcmbone

This file gives AI assistants (Claude Code and others) the context needed to work effectively in this repository.

---

## Project Overview

**edcmbone** is an early-stage monorepo implementing the **EDCM-PCNA-PCTA Framework** (Extended Distributed Cognitive Model with PCNA/PCTA framework). It consists of:

- A **Python backend** (`Backend/`) — core logic and transcript parsing
- A **React frontend** (`Frontend/`) — UI layer styled with Tailwind CSS
- An **AI Multimodel Hub** (`ammh/`) — sub-project for multi-model AI orchestration
- A **Tests** directory (`Tests/`) — test suite (currently being bootstrapped)
- A **Documentation** directory (`Documentation/`) — specs and design guidelines

**Current status**: Version 0.1.0. Most source files are stubs/placeholders. The project structure is established but active implementation is in progress.

---

## Repository Structure

```
edcmbone/
├── Backend/
│   ├── pyproject.toml          # Python package config (Hatchling build system)
│   ├── requirements.txt        # Runtime dependencies (populate as needed)
│   └── src/
│       └── edcmbone/
│           ├── __init__.py
│           └── parser/
│               └── turns_rounds.py   # Transcript parser (stub)
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
│   ├── spec.md                 # EDCM-PCNA-PCTA framework specification
│   ├── auth_testing.md         # Authentication testing notes
│   └── design_guidelines.json  # Design guidelines
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

The Python package is named `edcmbone`, importable as:
```python
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
- Package lives under `Backend/src/edcmbone/` — standard `src/` layout
- Python 3.8+ compatible code required (no 3.9+ syntax like `list[int]` type hints without `from __future__ import annotations`)
- `pyproject.toml` is the source of truth for metadata; `requirements.txt` is for direct runtime deps
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

## Important Files to Know

| File | Purpose |
|------|---------|
| `Backend/pyproject.toml` | Python package name, version, dependencies, build system |
| `Backend/src/edcmbone/parser/turns_rounds.py` | Core transcript parsing logic (primary backend entry point) |
| `Frontend/package.json` | Frontend dependencies and scripts |
| `ammh/backend/server.py` | AMMH multi-model hub server |
| `Documentation/spec.md` | Canonical framework specification (EDCM-PCNA-PCTA) — read this to understand domain concepts |
| `Tests/test_backend.py` | Backend test entry point |

---

## What Does Not Exist Yet (Do Not Assume)

- No CI/CD pipeline (no `.github/workflows/`)
- No environment variable file (`.env` or `.env.example`)
- No linting or formatting configs (`pyproject.toml [tool.ruff]`, `.eslintrc`, `.prettierrc`)
- No pre-commit hooks
- No pytest configuration (`pytest.ini` or `[tool.pytest.ini_options]`)
- `requirements.txt` is empty — add dependencies as they are introduced
- `tailwind.config.js` is empty — add `content` globs before using Tailwind classes

When implementing any of the above, use the most current conventions for the respective toolchain.

---

## Git Workflow

- Main branch: `master`
- Feature branches follow the pattern: `<type>/<description>-<id>` (e.g., `claude/add-claude-documentation-hl6si`)
- Commit messages should be clear and descriptive
- Author: Erin Patrick Spencer (erin.eps.hovel@gmail.com)
