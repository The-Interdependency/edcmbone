from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend_old" / "src"

# BACKEND_SRC must precede ROOT on sys.path: both contain an ``edcmbone``
# package, but only backend_old/src/edcmbone carries CanonLoader + metrics. ROOT
# stays on the path for the top-level test modules (core, engine, ucns_v04,
# closed_tokens); the repo-root ``edcmbone`` package is only ever loaded by
# tests under an explicit alias (see test_ucns_g_schema), never as ``edcmbone``.
for p in (str(ROOT), str(BACKEND_SRC)):   # insert ROOT first so BACKEND_SRC ends up ahead
    if p in sys.path:
        sys.path.remove(p)
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(BACKEND_SRC))
# The canonical edcmbone package lives under backend/src. Force it to the very
# front of sys.path (ahead of the repo root) so the incomplete repo-root
# edcmbone/ — the in-progress layer-migration target — cannot shadow it and
# break `from edcmbone.canon import CanonLoader`. The repo root stays on the
# path (after backend/src) because the package __init__ does
# `from version import __version__`, and version.py lives at the repo root.
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(BACKEND_SRC))
# Drop any shadow copy imported before this ran so the canonical one is cached.
sys.modules.pop("edcmbone", None)
import edcmbone  # noqa: E402,F401
