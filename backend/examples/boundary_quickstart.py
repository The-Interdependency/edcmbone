# ratios: loc_comments=13:6 imports_exports=3:1 calls_definitions=5:1
"""Copy-pasteable edcmbone-backend smoke demo.

Usage:
    python backend/examples/boundary_quickstart.py

If the backend is not installed, run this first from the repo root:
    python -m pip install -e backend
"""

from __future__ import annotations

import json

import edcmbone_backend as backend


def main() -> None:
    first = backend.make_boundary(
        "Delivered: backend can create a boundary object.",
        "Unresolved: wire this into the next UI or API surface.",
    )
    second = backend.make_boundary("Delivered: backend can compose boundaries.")
    merged = backend.merge_boundaries(first, second)
    print(json.dumps(backend.serialize_boundary(merged), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
# ratios: loc_comments=13:6 imports_exports=3:1 calls_definitions=5:1
