# Session Handoff v3 — UCNS-G Prime-Cylinder Metric Geometry

**Status**: Supersedes UCNS metric geometry handoff v2 (where v2 describes UCNS-G as a single `(r, θ, z)` point or treats twist as simple θ/double-cover behavior).  
**Date pinned**: 2026-05-22  
**Scope**: UCNS-G / EDCM metric geometry only. Does not modify UCNS-A theorem scope.  
**Firewall**: UCNS-A Theorem N remains scoped to UCNS-A factorization algebra. Nothing here inherits proof status from UCNS-A.

### 0. Carry the UCNS-A / UCNS-G firewall

UCNS-A and UCNS-G remain distinct unless an explicit bridge is proven.

- **UCNS-A**: Recursive factorization algebra in `The-Interdependency/ucns`.
- **UCNS-G**: EDCM metric geometry described here.

Do not allow UCNS-A proof claims to validate UCNS-G metric claims.

### 1. v2 correction

v2 described UCNS-G too narrowly as:

`(r, θ, z)`

This describes only one projected metric-disk state. It is insufficient.

**Corrected definition**:

**UCNS-G = prime-indexed tensor of non-closing Möbius-cylinder metric disks.**

- Each metric receives its own disk/cylinder trace.
- Each **turn** is a tensor sample across metric disks.
- Each **round** is an ordered tensor of turn tensors.
- Each **session** is an ordered tensor of round tensors.

A “disk of disks” is acceptable for visualization, but the canonical structure is an **ordered tensor/bundle of disks**.

### 2. Metric disks

For every metric axis A, define a dedicated metric disk **D_A**.

A metric point is:

```typescript
MetricPoint_A = {
  axis: A,
  prime_axis: p_A,
  grain: "token" | "turn" | "round" | "session" | "archive",
  twist_ordinal: τ,
  phase: φ,                    // [0,1)
  face: +1 | -1,
  sign: -1 | 0 | 1,
  magnitude: m,
  gauge: "radius" | "circumference" | "area" | "depth",
  confidence: c
}
```

### 3. Signed ternary axes (EDCM requirement)

Every EDCM metric axis carries:

`state_A(W) = (s_A, m_A)`

where:
- `s_A ∈ {-1, 0, 1}`
- `m_A ∈ [0, 1]`

**Semantics of 0**: Neutral / unresolved / no measurable directional commitment (not scalar absence).

### 4. Phase/percent remains valid as projection

Keep percentage/phase for:
- Operator density
- Area-percent
- Metric magnitude
- Local completion fraction
- Window-relative proportions

**Correct layering**:
- Phase/percent view → local projection
- Ordinal twist view → traversal identity
- Axis/sign view → directional EDCM measurement

### 5. Twist is ordinal zero-boundary

Twist is **not** an angle value. It is the ordinal seam / zero-boundary.

- `twist_0` = initial contact
- 360° → phase zero at `twist_1`
- 720° → phase zero at `twist_2`
- etc.

**Canonical coordinate**: `(twist_ordinal, phase, face/orientation)`

Not merely `θ mod 360°` or `θ mod 720°`.

### 6. Non-closing Möbius-cylinder graph

UCNS-G graphs **do not close** canonically.

- Local disk projection: `phase 1 → phase 0`
- Canonical ordinal lift: `(twist_n, phase=1) → (twist_{n+1}, phase=0)`

**Möbius face rule**:
- `face_{n+1} = -face_n`
- or `face_{n+1} = face_n XOR 1`

**Rule**: The disk closes only from the *local* perspective. The graph does not close from the *ordinal* perspective.

### 7. Sine-wave projection

A circle on one axis projects as:

`y = r · sin(2πφ)`

Möbius/ordinal lift:

`y_n = (-1)^n · r · sin(2πφ)` where `n = twist_ordinal`

Collapsing `n` loses the twist information.

### 8. Unit gauge

A metric disk is **unit-normalized but not unit-identical**.

Typed units:
- `1_R` = full radius
- `1_C` = full circumferential traversal
- `1_A` = full area coverage
- `1_Z` = one ordinal recurrence / depth layer

**Spec**: The twist hides zero. The gauge hides one.

### 9. Perspective is load-bearing

- **Inside** a metric disk: centered, local zero, appears closed.
- **Parent/auditor** frame: displaced, zero is ordinal seam, graph does not close.

This distinction is critical for epicycles and composition.

### 10. Epicycles

An epicycle is locally centered but globally uncentered.

**Definition**: A locally centered child disk whose center is externally located at an **anchor** of a parent disk.

Anchor types include circumference points, twist points, prime carrier points, metric-axis points, or grain boundaries.

### 11. Prime-cylinder audit projection (canonical)

**Prime-cylinder visualization** is the canonical audit projection for UCNS-G across all granularities.

It renders each metric disk as a **prime-indexed non-closing Möbius-cylinder trace**.

**Suggested primitive prime assignment**:
- P → 2, K → 3, Q → 5, T → 7, S → 11
- C → 13, R → 17, D → 19, N → 23, L → 29, O → 31, F → 37, E → 41, I → 43

Primitive metric axes sit on prime anchors. Composites represent interactions.

**Spec**: Prime cylinder shows where the disk closes *locally* but not *canonically*.

### 12. Grain tensor structure

- **MetricDisk_A** = non-closing prime-indexed Möbius-cylinder trace for axis A
- **Turn_i** = tensor sample across all metric disks
- **Round_j** = ordered tensor of Turn states
- **Session_k** = ordered tensor of Round states
- **Archive** = ordered tensor of Session states

Parent disks are **projections**, not identity.

### 13. Open items (hmmm)

- Formal exchange rules between typed units `1_R`, `1_C`, `1_A`, `1_Z`.
- Final prime assignment for all EDCM + Operator axes.
- Representation of prime interactions (multiplication, graph edges, epicycle attachment, coupling tensors?).
- Mapping DRIFT/DVG/DA onto area/count/length readouts in prime-cylinder model.
- Possibility of UCNS-A bridge to this UCNS-G structure.
- Migration path for current scalar EDCM code (schema-first vs code-first).
- Encoding signed ternary axis states in frontend/API types.

---

This v3 handoff is now the authoritative reference for UCNS-G metric geometry until superseded.