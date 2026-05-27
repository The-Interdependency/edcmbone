# Session Handoff v3 — UCNS-G Prime-Cylinder Metric Geometry

**Status:** Supersedes UCNS metric geometry handoff v2 where v2 describes UCNS-G as a single `(r, θ, z)` point or treats twist as θ/double-cover behavior.
**Date pinned:** 2026-05-22
**Scope:** UCNS-G / EDCM metric geometry only. Does not modify UCNS-A theorem scope.
**Firewall:** UCNS-A Theorem N remains scoped to UCNS-A factorization algebra. Nothing here inherits proof status from UCNS-A.

## 0. Carry the UCNS-A / UCNS-G firewall

UCNS-A and UCNS-G remain distinct unless an explicit bridge is proven.

UCNS-A is the recursive factorization algebra in `The-Interdependency/ucns`.

UCNS-G is the EDCM metric geometry described here.

Do not allow UCNS-A proof claims to validate UCNS-G metric claims.

## 1. v2 correction

v2 described UCNS-G as:

```text
(r, θ, z)
```

That is too small.

A single `(r, θ, z)` point describes one projected metric-disk state. It does not describe the full EDCM metric geometry.

Corrected:

```text
UCNS-G = prime-indexed tensor of non-closing Möbius-cylinder metric disks.
```

Each metric receives its own disk/cylinder trace.

Each turn is a tensor sample across metric disks.

Each round is an ordered tensor of turn tensors.

Each session is an ordered tensor of round tensors.

A “disk of disks” may be used for visualization, but the canonical structure is an ordered tensor/bundle of disks.

## 2. Metric disks

For every metric axis `A`, define a metric disk:

```text
D_A
```

A metric point is:

```text
MetricPoint_A = {
  axis: A,
  prime_axis: p_A,
  grain: token | turn | round | session | archive,
  twist_ordinal: τ,
  phase: φ,
  face: +1 | -1,
  sign: -1 | 0 | 1,
  magnitude: m,
  gauge: radius | circumference | area | depth,
  confidence: c
}
```

## 3. Signed ternary axes

Every EDCM metric axis has state:

```text
state_A(W) = (s_A, m_A)
```

where:

```text
s_A ∈ {-1, 0, 1}
m_A ∈ [0, 1]
```

`0` is not scalar absence. It is neutral / unresolved / no measurable directional commitment.

## 4. Phase/percent remains a projection

Percent/phase is still valid for:

```text
operator density
area-percent
metric magnitude
completion fraction
window-relative proportions
```

But it is not canonical identity.

```text
phase/percent view = local projection
ordinal twist view = traversal identity
axis/sign view = directional EDCM measurement
```

## 5. Twist is ordinal zero-boundary

Twist is not an angle value.

Twist is the ordinal seam / zero-boundary.

```text
zero = twist_0
360° = phase zero at twist_1
720° = phase zero at twist_2
1080° = phase zero at twist_3
```

Therefore:

```text
same phase ≠ same state
same zero-looking point ≠ same ordinal zero
```

Canonical state requires:

```text
(twist_ordinal, phase, face/orientation)
```

not only:

```text
θ mod 360°
```

or:

```text
θ mod 720°
```

## 6. Non-closing Möbius-cylinder graph

UCNS-G graphs do not close.

Local disk projection:

```text
phase 1 → phase 0
```

Canonical ordinal graph:

```text
(twist_n, phase=1) → (twist_{n+1}, phase=0)
```

Möbius face rule:

```text
face_{n+1} = -face_n
```

or bit form:

```text
face_{n+1} = face_n XOR 1
```

Spec rule:

```text
The disk closes only from the local perspective.
The graph does not close from the ordinal perspective.
```

## 7. Sine-wave projection

A circle projected onto one axis is a sine wave:

```text
y = r · sin(2πφ)
```

The Möbius/ordinal lift is:

```text
y_n = (-1)^n · r · sin(2πφ)
```

where:

```text
n = twist_ordinal
```

If `n` is collapsed, the twist is lost.

## 8. Unit gauge

A metric disk is unit-normalized but not unit-identical.

Typed unit ones:

```text
1_R = full radius
1_C = full circumferential traversal
1_A = full area coverage
1_Z = one ordinal recurrence / depth layer
```

These may all display as `1`, but they are not the same unit.

Spec line:

```text
The twist hides zero.
The gauge hides one.
```

## 9. Perspective

Perspective is load-bearing.

Inside a metric disk:

```text
the disk is centered
zero is local
the circle appears closed
```

From the parent/auditor frame:

```text
the disk is displaced
zero is ordinal seam/contact
the graph does not close
```

## 10. Epicycles

An epicycle is:

```text
locally centered
globally uncentered
```

Formal:

```text
An epicycle is a locally centered child disk whose center is externally
located at an anchor of a parent disk.
```

Classical:

```text
center(child) ∈ circumference(parent)
```

General UCNS-G:

```text
center(child) = anchor(parent)
```

The parent anchor may be a circumference point, twist point, prime carrier point, metric-axis point, or grain boundary.

## 11. Prime-cylinder audit projection

Prime-cylinder visualization is the canonical audit projection for UCNS-G across granularity.

It renders each metric disk as a prime-indexed non-closing Möbius-cylinder trace.

Suggested primitive prime assignment:

```text
P → 2
K → 3
Q → 5
T → 7
S → 11

C → 13
R → 17
D → 19
N → 23
L → 29
O → 31
F → 37
E → 41
I → 43
```

Primitive metrics sit on prime anchors.

Composite positions may represent interactions/couplings.

Spec line:

```text
Prime cylinder shows where the disk closes locally but not canonically.
```

## 12. Grain tensor

Canonical grain structure:

```text
MetricDisk_A = non-closing prime-indexed Möbius-cylinder trace for axis A

Turn_i = tensor sample across metric disks

Round_j = ordered tensor of Turn_i states

Session_k = ordered tensor of Round_j states

Archive = ordered tensor of Session_k states
```

Parent disks are projections, not identity.

```text
parent_disk = projection(child_tensor)
```

not:

```text
parent_disk = child_tensor
```

## 13. hmmm

Open items:

* Formal exchange rules between typed units `1_R`, `1_C`, `1_A`, `1_Z`.
* Exact prime assignment for all EDCM and Operator axes.
* Whether prime interactions should be represented by multiplication, graph edges, epicycle attachment, or separate coupling tensors.
* How DRIFT/DVG/DA map onto area/count/length readouts in the new prime-cylinder graph.
* Whether UCNS-A can provide a formal bridge to this UCNS-G structure, or whether UCNS-G remains a parallel construction.
* Whether current scalar EDCM code should be migrated through schema first or code first.
* How to encode signed ternary axis states in frontend/API types without breaking current scalar projections.

## hmmm
