// edcmbone/frontend/src/ucns_g/types.ts
// UCNS-G v3 metric-geometry schema (TypeScript companion).
//
// Mirrors edcmbone/edcmbone/ucns_g/schema.py. See
// docs/handoffs/2026-05-22-ucns-g-prime-cylinder-v3.md for the canonical
// specification.
//
// UCNS-A / UCNS-G firewall: nothing here inherits proof status from UCNS-A.

// ---------------------------------------------------------------------------
// Axis identifiers
// ---------------------------------------------------------------------------

// Operator-layer (PKQTS) primitive metric axes.
export type OperatorAxis = "P" | "K" | "Q" | "T" | "S";

// EDCM behavioral primitive metric axes.
export type EdcmAxis =
  | "C" | "R" | "D" | "N" | "L" | "O" | "F" | "E" | "I";

export type MetricAxis = OperatorAxis | EdcmAxis;

// ---------------------------------------------------------------------------
// Grain hierarchy
// ---------------------------------------------------------------------------

export type Grain = "token" | "turn" | "round" | "session" | "archive";

export const GRAIN_ORDER: ReadonlyArray<Grain> = [
  "token",
  "turn",
  "round",
  "session",
  "archive",
];

// ---------------------------------------------------------------------------
// Signed ternary axis state
// ---------------------------------------------------------------------------

// -1 opposing/contracting/resolving/suppressing direction
//  0 neutral / unresolved / no measurable directional commitment
// +1 activating/expanding/expressing direction
//
// Pin: 0 is not scalar nothing. It is a neutral/uncommitted axis state.
export type AxisSign = -1 | 0 | 1;

// ---------------------------------------------------------------------------
// Möbius face / orientation bit
// face_{n+1} = -face_n   (or, bit form: face_{n+1} = face_n XOR 1)
// ---------------------------------------------------------------------------

export type Face = -1 | 1;

// ---------------------------------------------------------------------------
// Typed unit gauge
// ---------------------------------------------------------------------------

// A metric disk is unit-normalized but not unit-identical:
//   1_R = full radius
//   1_C = full circumferential traversal
//   1_A = full area coverage
//   1_Z = one ordinal recurrence / depth layer
//
// All four can display as 1, but they are different unit bases.
export type GaugeKind = "radius" | "circumference" | "area" | "depth";

export type UnitGauge = {
  kind: GaugeKind;
  // Magnitude expressed in the named unit basis. Display value 1 is the
  // normalized full unit. Carried as a rational tuple [num, den] to avoid
  // floating-point drift; receivers that don't need rationals may collapse
  // to num / den.
  value: readonly [num: number, den: number];
};

export const ONE_R: UnitGauge = { kind: "radius", value: [1, 1] };
export const ONE_C: UnitGauge = { kind: "circumference", value: [1, 1] };
export const ONE_A: UnitGauge = { kind: "area", value: [1, 1] };
export const ONE_Z: UnitGauge = { kind: "depth", value: [1, 1] };

// ---------------------------------------------------------------------------
// Metric disk state
// ---------------------------------------------------------------------------

// Mirrors the v3 handoff sketch.
//
// twist_ordinal: ordinal seam (twist_0, twist_1, ...). NOT an angle value.
// phase:         normalized local phase, half-open [0, 1).
// face:          -1 or +1; advances as face_{n+1} = -face_n across twists.
// sign:          signed ternary {-1, 0, +1}; 0 is neutral, not absence.
// magnitude:     in [0, 1] — the local phase/percent projection.
// gauge:         which typed unit-one basis this disk is denominated in.
// confidence:    optional, in [0, 1] when present.
export type MetricDiskState = {
  axis: MetricAxis;
  primeAxis: number;
  grain: Grain;
  twistOrdinal: number;
  phase: number;
  face: Face;
  sign: AxisSign;
  magnitude: number;
  gauge: GaugeKind;
  confidence?: number;
};

// Handoff naming parity: MetricPoint is the wire-name in the sketch.
export type MetricPoint = MetricDiskState;

// ---------------------------------------------------------------------------
// Grain tensor
// ---------------------------------------------------------------------------

// From the v3 handoff:
//   MetricDisk_A = non-closing prime-indexed Möbius-cylinder trace for axis A
//   Turn_i       = tensor sample across metric disks
//   Round_j      = ordered tensor of Turn_i states
//   Session_k    = ordered tensor of Round_j states
//   Archive      = ordered tensor of Session_k states
//
// Parent disks are projections, not identity:
//   parent_disk = projection(child_tensor)
//   not:
//   parent_disk = child_tensor
export type GrainTensor = {
  grain: Grain;
  states: ReadonlyArray<MetricDiskState>;
};

// ---------------------------------------------------------------------------
// Prime-axis assignment
// ---------------------------------------------------------------------------

export const PRIME_AXIS_ASSIGNMENT: Readonly<Record<MetricAxis, number>> = {
  // Operator layer
  P: 2,
  K: 3,
  Q: 5,
  T: 7,
  S: 11,
  // EDCM behavioral layer
  C: 13,
  R: 17,
  D: 19,
  N: 23,
  L: 29,
  O: 31,
  F: 37,
  E: 41,
  I: 43,
};

export const PRIMITIVE_OPERATOR_AXES: ReadonlyArray<OperatorAxis> = [
  "P", "K", "Q", "T", "S",
];

export const PRIMITIVE_METRIC_AXES: ReadonlyArray<EdcmAxis> = [
  "C", "R", "D", "N", "L", "O", "F", "E", "I",
];

export function primeForAxis(axis: MetricAxis): number {
  return PRIME_AXIS_ASSIGNMENT[axis];
}
