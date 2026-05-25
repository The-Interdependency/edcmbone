"""
edcmbone.ucns_g.schema
~~~~~~~~~~~~~~~~~~~~~~

Frozen dataclass schemas for UCNS-G v3.

Mirrors the Python sketch from the v3 handoff:

    MetricAxis            — string identifier for an EDCM or Operator axis
    Grain                 — token | turn | round | session | archive
    AxisSign              — -1 | 0 | 1   (0 is neutral, not absence)
    Face                  — -1 | +1      (Möbius face / orientation bit)
    GaugeKind             — radius | circumference | area | depth
    UnitGauge             — typed unit-one: (kind, value)
    MetricDiskState       — full disk-state record for one axis at one grain
    MetricPoint           — alias for MetricDiskState (handoff naming parity)
    GrainTensor           — ordered tensor of states across the grain hierarchy

All numeric magnitudes use ``fractions.Fraction`` so phase / magnitude /
gauge values do not silently drift through floating-point rounding when
composed across grains.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Tuple

try:
    from typing import Literal
except ImportError:  # pragma: no cover - Python 3.7 fallback
    from typing_extensions import Literal  # type: ignore[no-redef]


# ---------------------------------------------------------------------------
# Axis identifiers
# ---------------------------------------------------------------------------

# Operator (PKQTS) axes — primitive metric-axis identities at the Operator layer.
# Semantic labels follow the v3 handoff (not the prior bone-family labels):
#   P → Polarity / Conflict
#   K → Linkage / Relation
#   Q → Inquiry / Gap
#   T → Temporal / Modality
#   S → Structural / Referential
OperatorAxis = Literal["P", "K", "Q", "T", "S"]

# EDCM behavioral metric axes.
#   C → Constraint
#   R → Refusal
#   D → Deflection
#   N → Noise
#   L → Resistance       (pinned by v2; carried forward)
#   O → Signed axis      (pinned by v2; carried forward, ranges over -1..+1)
#   F → Fixation
#   E → Escalation
#   I → Integration-failure
EdcmAxis = Literal["C", "R", "D", "N", "L", "O", "F", "E", "I"]

MetricAxis = Literal[
    "P", "K", "Q", "T", "S",
    "C", "R", "D", "N", "L", "O", "F", "E", "I",
]


# ---------------------------------------------------------------------------
# Grain hierarchy
# ---------------------------------------------------------------------------

Grain = Literal["token", "turn", "round", "session", "archive"]

GRAIN_ORDER: Tuple[Grain, ...] = ("token", "turn", "round", "session", "archive")


# ---------------------------------------------------------------------------
# Signed ternary axis state
# ---------------------------------------------------------------------------

# AxisSign: -1 opposing/contracting/resolving/suppressing direction
#            0 neutral/absent/unresolved/no measurable directional commitment
#           +1 activating/expanding/expressing direction
#
# Pin: 0 is not scalar nothing. It is a neutral/uncommitted axis state.
AxisSign = Literal[-1, 0, 1]


# ---------------------------------------------------------------------------
# Möbius face / orientation bit
# ---------------------------------------------------------------------------

# face_{n+1} = -face_n   (XOR-form: face_{n+1} = face_n XOR 1)
Face = Literal[-1, 1]


# ---------------------------------------------------------------------------
# Typed unit gauge
# ---------------------------------------------------------------------------

# A metric disk is unit-normalized but not unit-identical.
# Typed unit ones:
#   1_R = full radius
#   1_C = full circumferential traversal
#   1_A = full area coverage
#   1_Z = one ordinal recurrence / depth layer
#
# These may all display as 1, but they are not the same unit.
GaugeKind = Literal["radius", "circumference", "area", "depth"]


@dataclass(frozen=True)
class UnitGauge:
    """Typed unit-one carrier.

    ``kind`` identifies which unit basis the value is denominated in.
    ``value`` is the magnitude expressed in that basis (display value 1
    is the normalized full unit, but values may be any Fraction in [0, 1]
    or beyond for over-traversal).
    """

    kind: GaugeKind
    value: Fraction = Fraction(1)

    # Convenience constructors mirroring the spec's typed-one symbols.

    @classmethod
    def one_R(cls) -> "UnitGauge":
        return cls(kind="radius", value=Fraction(1))

    @classmethod
    def one_C(cls) -> "UnitGauge":
        return cls(kind="circumference", value=Fraction(1))

    @classmethod
    def one_A(cls) -> "UnitGauge":
        return cls(kind="area", value=Fraction(1))

    @classmethod
    def one_Z(cls) -> "UnitGauge":
        return cls(kind="depth", value=Fraction(1))


# ---------------------------------------------------------------------------
# Metric disk state
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class MetricDiskState:
    """Single metric-disk sample for axis ``axis`` at grain ``grain``.

    Mirrors the v3 handoff sketch:

        MetricPoint_A = {
            axis,
            prime_axis,
            grain,
            twist_ordinal,
            phase,
            face,
            sign,
            magnitude,
            gauge,
            confidence,
        }

    Notes:
        - ``twist_ordinal`` is the ordinal seam (twist_0, twist_1, ...).
          It is not an angle value.
        - ``phase`` is normalized local phase in [0, 1).
        - ``face`` is -1 or +1, advancing as face_{n+1} = -face_n across
          twist ordinals.
        - ``sign`` is signed ternary {-1, 0, +1}; 0 is neutral, not absent.
        - ``magnitude`` is in [0, 1] (the phase / percent projection).
        - ``gauge`` records which typed unit-one basis this disk is
          denominated in.
        - ``confidence`` is optional; ``None`` means unspecified.
    """

    axis: MetricAxis
    prime_axis: int
    grain: Grain
    twist_ordinal: int
    phase: Fraction
    face: Face
    sign: AxisSign
    magnitude: Fraction
    gauge: GaugeKind
    confidence: "Fraction | None" = None

    def __post_init__(self) -> None:
        # Validate at construction time; this is a frozen dataclass so
        # later mutation is not possible.
        if self.twist_ordinal < 0:
            raise ValueError(
                f"twist_ordinal must be >= 0, got {self.twist_ordinal!r}"
            )
        if not (Fraction(0) <= self.phase < Fraction(1)):
            raise ValueError(
                f"phase must be in [0, 1), got {self.phase!r}"
            )
        if self.face not in (-1, 1):
            raise ValueError(f"face must be -1 or +1, got {self.face!r}")
        if self.sign not in (-1, 0, 1):
            raise ValueError(
                f"sign must be -1, 0, or +1, got {self.sign!r}"
            )
        if not (Fraction(0) <= self.magnitude <= Fraction(1)):
            raise ValueError(
                f"magnitude must be in [0, 1], got {self.magnitude!r}"
            )
        if self.gauge not in ("radius", "circumference", "area", "depth"):
            raise ValueError(f"unknown gauge kind: {self.gauge!r}")
        if self.grain not in GRAIN_ORDER:
            raise ValueError(f"unknown grain: {self.grain!r}")
        if self.prime_axis < 2:
            raise ValueError(
                f"prime_axis must be a prime >= 2, got {self.prime_axis!r}"
            )
        if self.confidence is not None and not (
            Fraction(0) <= self.confidence <= Fraction(1)
        ):
            raise ValueError(
                f"confidence must be in [0, 1] or None, got {self.confidence!r}"
            )


# Handoff naming parity: MetricPoint is the wire-name in the v3 sketch.
# Internally we treat MetricPoint and MetricDiskState as the same record.
MetricPoint = MetricDiskState


# ---------------------------------------------------------------------------
# Grain tensor
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GrainTensor:
    """Ordered tensor of metric-disk states across the grain hierarchy.

    From the v3 handoff:

        MetricDisk_A = non-closing prime-indexed Möbius-cylinder trace for axis A
        Turn_i       = tensor sample across metric disks
        Round_j      = ordered tensor of Turn_i states
        Session_k    = ordered tensor of Round_j states
        Archive      = ordered tensor of Session_k states

    Parent disks are projections, not identity:
        parent_disk = projection(child_tensor)
        not:
        parent_disk = child_tensor

    This dataclass stores the *child* states at the indicated grain. The
    parent-projection is computed elsewhere; storing the projection here
    would collapse the twist ordinal and lose information.
    """

    grain: Grain
    states: Tuple[MetricDiskState, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.grain not in GRAIN_ORDER:
            raise ValueError(f"unknown grain: {self.grain!r}")
        for s in self.states:
            if not isinstance(s, MetricDiskState):
                raise TypeError(
                    f"GrainTensor.states must contain MetricDiskState, "
                    f"got {type(s).__name__}"
                )
