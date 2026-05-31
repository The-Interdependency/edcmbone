from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"

# BACKEND_SRC must precede ROOT on sys.path: both contain an ``edcmbone``
# package, but only backend/src/edcmbone carries CanonLoader + metrics. ROOT
# stays on the path for the top-level test modules (core, engine, ucns_v04,
# closed_tokens); the repo-root ``edcmbone`` package is only ever loaded by
# tests under an explicit alias (see test_ucns_g_schema), never as ``edcmbone``.
for p in (str(ROOT), str(BACKEND_SRC)):   # insert ROOT first so BACKEND_SRC ends up ahead
    if p in sys.path:
        sys.path.remove(p)
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(BACKEND_SRC))
