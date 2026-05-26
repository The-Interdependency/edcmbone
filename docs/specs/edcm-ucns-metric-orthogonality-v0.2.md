# EDCM / UCNS Metric Orthogonality Spec v0.2

**Status:** draft  
**Scope:** UCNS construction of EDCM metric objects  
**Primary doctrine:** UCNS exists to construct EDCM metrics.

## 1. Metric axis state

Every EDCM metric axis is a signed ternary UCNS axis:

```text
AxisState_A = (s_A, m_A)

s_A ∈ {-1, 0, +1}
m_A ∈ [0, 1]
```

```text
-1 = negative / opposing / reducing / reversing direction
 0 = neutral / stable / unresolved directional commitment
+1 = positive / activating / increasing / aligned direction
```

```text
NA ≠ 0
```

```text
NA = readout disabled because required field/context is absent
0  = field/context exists and the axis is neutral
```

UCNS-G pins signed ternary axis state as `s ∈ {-1,0,+1}`, with `0` meaning neutral rather than absence.

## 2. Object layers

```text
ConstraintField_t
FieldMotion_{t-1→t}
MetricAxis_A
MetricValue_A,t
MetricCoupling_X
MetricProjection_Y
```

## 3. ConstraintField

```text
schema_id: edcm/constraint_field_ucns_v1
object_kind: constraint_field
grain: token | turn | round | session | archive
```

A `ConstraintField_t` contains:

```text
field_obj
engagement_obj
field_hash
presence_substrate
contact_state
resolution_state
witness
```

The current bridge (v0.1 adapter) encodes a round into `field_obj` and `engagement_obj`; presence is audited through intrinsic carrier geometry, contact through engagement/face state, and resolution through payload state.

## 4. ConstraintField readouts

### 4.1 Presence substrate

```text
presence_substrate = intrinsic carrier / raised-field geometry
```

```text
presence_substrate is not itself L.
presence_substrate supports L readouts.
```

Empty field rule:

```text
if raised_field_count = 0:
    contact = NA
    L = NA
    D = NA
    R = NA
    I = NA
```

Bridge smoke tests pin empty-field NA behavior and carrier-derived presence.

### 4.2 Contact

```text
contact_state = (s_contact, m_contact)

s_contact ∈ {-1, 0, +1}
m_contact ∈ [0, 1]
```

```text
-1 = against / opposing contact
 0 = neutral / no effective directional contact
+1 = toward / aligned contact
```

Adapter vocabulary mapping (v0.1):

```text
away     -> contact_state = 0 with deflection signal
toward   -> contact_state = +1
against  -> contact_state = -1
```

### 4.3 Resolution / integration

```text
resolution_state = (s_resolution, m_resolution)

s_resolution ∈ {-1, 0, +1}
m_resolution ∈ [0, 1]
```

```text
-1 = dis-integration / failed incorporation / opened constraint
 0 = unresolved / no testable resolution movement
+1 = integration / closure / accepted resolution
```

Adapter mapping:

```text
payload None      -> accepted / closed
payload non-unit  -> accommodated / open
```

## 5. FieldMotion

```text
schema_id: edcm/field_motion_ucns_v1
object_kind: field_motion
previous_field_hash
current_field_hash
```

```text
FieldMotion_{t-1→t} = relation(ConstraintField_{t-1}, ConstraintField_t)
```

F, E, and O_scope are signed ternary right-angle readouts of `FieldMotion`.

```text
F = recurrence ↔ release
E = escalation ↔ de-escalation
O = expansion ↔ contraction
```

## 6. F / E / O_scope triad

### 6.1 F — fixation / recurrence

```text
F_state = (s_F, m_F)

-1 = release / de-fixation
 0 = stable recurrence
+1 = fixation / recurrence increase
```

Reads:

```text
repeated anchors
repeated contact pattern
repeated open payload
repeated sequence signature
```

### 6.2 E — escalation / intensification

```text
E_state = (s_E, m_E)

-1 = de-escalation
 0 = stable intensity
+1 = escalation
```

Reads:

```text
contact force delta
against delta
unresolved delta
urgency delta
pressure delta
```

### 6.3 O_scope — scope motion

```text
O_scope_state = (s_O_scope, m_O_scope)

-1 = contraction / narrowing
 0 = stable boundary
+1 = expansion / overextension
```

Reads:

```text
new anchors
out-of-field anchors
boundary delta
branch count delta
scope delta
```

## 7. O split

```text
O_scope ≠ O_confidence
```

### 7.1 O_scope

```text
metric_id: edcm.behavioral.O_scope
axis: scope motion
parent: FieldMotion
state: (-1,0,+1), magnitude [0,1]
```

### 7.2 O_confidence

```text
metric_id: edcm.behavioral.O_confidence
axis: confidence polarity
parent: confidence evidence object
state: (-1,0,+1), magnitude [0,1]
```

```text
-1 = underconfidence / collapse / excessive hedging
 0 = calibrated confidence
+1 = overconfidence / overclaiming
```

## 8. L split

```text
L_load ≠ L_loss ≠ L_resistance
```

### 8.1 L_load

```text
metric_id: edcm.behavioral.L_load
axis: constraint load
parent: ConstraintField
state: (-1,0,+1), magnitude [0,1]
```

```text
-1 = load reducing
 0 = stable load
+1 = load increasing
```

### 8.2 L_loss

```text
metric_id: edcm.behavioral.L_loss
axis: coherence loss
parent: sequence / continuity evidence
state: (-1,0,+1), magnitude [0,1]
```

```text
-1 = coherence recovering
 0 = stable coherence
+1 = coherence degrading
```

### 8.3 L_resistance

```text
metric_id: edcm.behavioral.L_resistance
axis: resistance pressure
parent: ConstraintField / Contact
state: (-1,0,+1), magnitude [0,1]
```

```text
-1 = resistance softening
 0 = stable resistance
+1 = resistance hardening
```

## 9. Metric registry

| ID                                    | Symbol | Axis                             | Parent object                | State          |
| ------------------------------------- | -----: | -------------------------------- | ---------------------------- | -------------- |
| `edcm.behavioral.C.constraint_strain` |      C | constraint strain                | ConstraintField / evidence   | signed ternary |
| `edcm.behavioral.R.refusal_density`   |      R | refusal / resistance contact     | ConstraintField / Contact    | signed ternary |
| `edcm.behavioral.D.deflection`        |      D | deflection / return              | ConstraintField / Contact    | signed ternary |
| `edcm.behavioral.I.integration`       |      I | integration / dis-integration    | ConstraintField / Resolution | signed ternary |
| `edcm.behavioral.F.fixation`          |      F | recurrence / release             | FieldMotion                  | signed ternary |
| `edcm.behavioral.E.escalation`        |      E | escalation / de-escalation       | FieldMotion                  | signed ternary |
| `edcm.behavioral.O_scope`             |      O | expansion / contraction          | FieldMotion                  | signed ternary |
| `edcm.behavioral.O_confidence`        |      O | confidence polarity              | confidence evidence          | signed ternary |
| `edcm.behavioral.L_load`              |      L | load increase / decrease         | ConstraintField              | signed ternary |
| `edcm.behavioral.L_loss`              |      L | coherence loss / recovery        | continuity evidence          | signed ternary |
| `edcm.behavioral.L_resistance`        |      L | resistance hardening / softening | ConstraintField / Contact    | signed ternary |
| `edcm.behavioral.N.noise`             |      N | signal efficiency / inefficiency | system evidence              | signed ternary |
| `edcm.round.P_progress`               |      P | progress / regression            | sequence state               | signed ternary |
| `edcm.state.kappa`                    |      κ | stored tension / release         | state composite              | signed ternary |

## 10. Projection registry

Layer 3 outputs are projections, not primitive axes.

| ID                      | Symbol | Definition                        |
| ----------------------- | -----: | --------------------------------- |
| `edcm.projection.CM`    |     CM | projection over C and I           |
| `edcm.projection.DA`    |     DA | projection over κ, E, R           |
| `edcm.projection.DRIFT` |  DRIFT | projection over L and P           |
| `edcm.projection.DVG`   |    DVG | projection over D and N           |
| `edcm.projection.INT`   |    INT | projection over E and F           |
| `edcm.projection.TBF`   |    TBF | speaker-share fairness projection |

## 11. Orthogonality rules

```text
A primitive metric axis must have:

1. unique metric_id
2. unique UCNS axis object
3. signed ternary state
4. declared parent object
5. declared semantic axis
6. declared magnitude rule
7. declared NA rule
8. explicit coupling if it shares evidence or depends on another readout
```

```text
A scalar formula that depends on another metric score is not primitive.
It is a coupling or projection.
```

```text
A bare symbol is not canonical identity.
```

## 12. Current required canonical separations

```text
contact_state is signed ternary, not away/toward/against labels.
```

```text
L_load, L_loss, and L_resistance are distinct axes unless explicitly aliased.
```

```text
O_scope and O_confidence are distinct axes.
```

```text
P_progress is not Operator P.
```

```text
κ is state_composite, not primitive metric.
```

```text
E_current = R + loop_risk is compatibility coupling, not primitive E.
```

## 13. F / E / O fixture matrix

| Fixture              |  F |  E | O_scope |
| -------------------- | -: | -: | ------: |
| `stable_resolution`  | -1 | -1 |       0 |
| `stuck_loop`         | +1 |  0 |       0 |
| `sharp_spike`        |  0 | +1 |       0 |
| `scope_contraction`  |  0 |  0 |      -1 |
| `scope_creep`        |  0 |  0 |      +1 |
| `escalating_loop`    | +1 | +1 |       0 |
| `sprawling_loop`     | +1 |  0 |      +1 |
| `pressure_sprawl`    |  0 | +1 |      +1 |
| `runaway_spiral`     | +1 | +1 |      +1 |
| `decompressing_loop` | -1 | -1 |      -1 |

## 14. Test obligations

```text
1. Empty field produces NA, not 0.
2. Zero state requires field/context presence.
3. Every axis object has signed ternary state.
4. Contact axis uses -1/0/+1.
5. L axes use -1/0/+1.
6. O axes use -1/0/+1.
7. O_scope hash != O_confidence hash.
8. L_load hash != L_loss hash unless explicit alias object exists.
9. F/E/O_scope share FieldMotion parent hash for same transition.
10. F/E/O_scope axis hashes are distinct.
11. P_progress hash != Operator P hash.
12. κ marked state_composite.
13. Projection objects not marked primitive.
```

## 15. One-line spec

```text
EDCM is one evolving UCNS field whose metric axes are signed ternary readouts:
ConstraintField supplies state readouts, FieldMotion supplies F/E/O motion
readouts, N/P/κ supply system-state readouts, and Layer 3 values are projections;
orthogonality means distinct UCNS axes with explicit coupling, not independent
scalar formulas.
```

## Push checklist

- [x] Contact is specified as -1/0/+1, not away/toward/against.
- [x] L_load, L_loss, L_resistance are signed ternary.
- [x] O_scope and O_confidence are signed ternary and distinct.
- [x] NA is explicitly different from 0.
- [x] ConstraintField is state object.
- [x] FieldMotion is tangent/differential object.
- [x] F/E/O_scope are FieldMotion readouts.
- [x] P_progress is not Operator P.
- [x] κ is state composite.
- [x] Projections are not primitive axes.
- [x] Uploaded bridge is referenced as v0.1 adapter, not final canonical vocabulary.
