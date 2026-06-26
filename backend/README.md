# edcmbone-backend

This backend is intentionally small: the active backend package imports only
`ucns`. It turns unresolved constraints into explicit boundary objects rather
than silently resolving them.

The prior backend has been preserved at `backend_old/`.

## Few-click path

From the repository root:

```bash
python -m pip install -e backend
python backend/examples/boundary_quickstart.py
```

Expected result: a JSON object with `delivered`, structured `hmmm`, and `ucns`
fields. If that prints, the backend is installed and usable.

## Usage Guidance

After installation, use the backend directly:

```python
import edcmbone_backend as backend

boundary = backend.make_boundary(
    "delivered output",
    "remaining constraint to carry forward",
)
print(backend.serialize_boundary(boundary))
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

- Runtime dependency boundary: active backend source imports only `ucns`.
- Packaging boundary: the backend wheel includes a local `ucns` package so users
  do not need to put the repository root on `PYTHONPATH`.
- Risk boundary: in-memory only; no auth, storage, network, admin, or secret
  side effects.
- Documentation and runtime boundaries are declared in msdmd blocks beside the
  implementation, following `The-Interdependency/skill-lib` canonical guidance.
