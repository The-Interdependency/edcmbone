# edcmbone-backend

This backend is intentionally small: its only runtime import is `ucns`.
It turns unresolved constraints into explicit boundary objects rather than
silently resolving them.

The prior backend has been preserved at `backend_old/`.

## Usage Guidance

Install or run from this repository with both the repository root and backend
source path on `PYTHONPATH` so the backend can import the UCNS compatibility
module:

```bash
PYTHONPATH="$PWD:$PWD/backend/src" python - <<'PY'
import edcmbone_backend as backend

boundary = backend.make_boundary(
    "delivered output",
    "remaining constraint to carry forward",
)
print(backend.serialize_boundary(boundary))
PY
```

### Boundary lifecycle

1. Use `make_boundary(delivered, unresolved)` when producing output that may
   leave a constraint unresolved.
2. Use `boundary.hmmm` as the mandatory transition object between delivered
   output and living continuation. If `unresolved` is empty, it still carries a
   truthful fallback note.
3. Use `merge_boundaries(left, right)` when composing two boundary-producing
   steps; the function preserves both `hmmm` records and composes their UCNS
   carriers with `ucns.multiply`.
4. Use `serialize_boundary(boundary)` at API or persistence edges. The backend
   itself does not import JSON, perform network I/O, or write storage.

### Integration notes

- Runtime dependency boundary: backend source imports only `ucns`.
- Risk boundary: in-memory only; no auth, storage, network, admin, or secret
  side effects.
- Documentation and runtime boundaries are declared in msdmd blocks beside the
  implementation, following `The-Interdependency/skill-lib` canonical guidance.
