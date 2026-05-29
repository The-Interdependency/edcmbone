"""
edcmbone.ucns_g.schema
~~~~~~~~~~~~~~~~~~~~~~

Frozen dataclass schemas for UCNS-G v3.

Mirrors the Python sketch from the v3 handoff:

    MetricAxis            — string identifier for an EDCM or Operator axis
    Grain                 — token | turn | round | session | archive
    AxisSign              — -1 | 0 | 1   (0 is neutral, not absence)
    AxisState             — state_A(W) = (sign, magnitude)
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

from .primes import prime_for_axis


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


@dataclass(frozen=True)
class AxisState:
    """Signed ternary EDCM state ``state_A(W) = (s_A, m_A)``.

    ``sign`` is directional commitment in ``{-1, 0, +1}``; ``0`` is a
    measurable neutral/uncommitted state, not absence. ``magnitude`` is the
    normalized scalar projection in ``[0, 1]``.
    """

    sign: AxisSign
    magnitude: Fraction

    def __post_init__(self) -> None:
        magnitude = _as_fraction(self.magnitude, "magnitude")
        object.__setattr__(self, "magnitude", magnitude)
        if self.sign not in (-1, 0, 1):
            raise ValueError(f"sign must be -1, 0, or +1, got {self.sign!r}")
        _validate_unit_interval(magnitude, "magnitude")


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
VALID_GAUGE_KINDS: Tuple[GaugeKind, ...] = (
    "radius",
    "circumference",
    "area",
    "depth",
)


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

    def __post_init__(self) -> None:
        if self.kind not in VALID_GAUGE_KINDS:
            raise ValueError(f"unknown gauge kind: {self.kind!r}")
        object.__setattr__(self, "value", _as_fraction(self.value, "value"))

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


def _as_fraction(value: object, field_name: str) -> Fraction:
    """Coerce exact numeric inputs to ``Fraction`` for stable schema values."""

    try:
        return value if isinstance(value, Fraction) else Fraction(value)  # type: ignore[arg-type]
    except (TypeError, ValueError, ZeroDivisionError) as exc:
        raise TypeError(f"{field_name} must be Fraction-compatible, got {value!r}") from exc


def _validate_unit_interval(value: Fraction, field_name: str) -> None:
    if not (Fraction(0) <= value <= Fraction(1)):
        raise ValueError(f"{field_name} must be in [0, 1], got {value!r}")


def _validate_twist_ordinal(twist_ordinal: int) -> None:
    if isinstance(twist_ordinal, bool) or not isinstance(twist_ordinal, int):
        raise TypeError(
            f"twist_ordinal must be a nonnegative int, got {twist_ordinal!r}"
        )
    if twist_ordinal < 0:
        raise ValueError(f"twist_ordinal must be >= 0, got {twist_ordinal!r}")


def mobius_face_for_twist(twist_ordinal: int, initial_face: Face = 1) -> Face:
    """Return the canonical Möbius face for ``twist_ordinal``.

    This encodes the v3 rule ``face_{n+1} = -face_n`` without treating twist
    as an angle. The default starts at ``+1`` for ``twist_0``.
    """

    _validate_twist_ordinal(twist_ordinal)
    if initial_face not in (-1, 1):
        raise ValueError(f"initial_face must be -1 or +1, got {initial_face!r}")
    return initial_face if twist_ordinal % 2 == 0 else -initial_face  # type: ignore[return-value]


def split_ordinal_phase(
    traversal: Fraction,
    *,
    initial_twist: int = 0,
) -> Tuple[int, Fraction]:
    """Split a nonnegative traversal count into ``(twist_ordinal, phase)``.

    ``traversal`` counts local disk traversals where each whole unit advances
    the ordinal seam. For example, ``0`` maps to ``(0, 0)``, ``1`` maps to
    ``(1, 0)``, and ``Fraction(5, 2)`` maps to ``(2, Fraction(1, 2))``.
    """

    _validate_twist_ordinal(initial_twist)
    traversal = _as_fraction(traversal, "traversal")
    if traversal < 0:
        raise ValueError(f"traversal must be >= 0, got {traversal!r}")
    whole = traversal.numerator // traversal.denominator
    phase = traversal - whole
    return initial_twist + whole, phase


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
        expected_prime = prime_for_axis(self.axis)
        if self.prime_axis != expected_prime:
            raise ValueError(
                f"prime_axis for axis {self.axis!r} must be {expected_prime}, "
                f"got {self.prime_axis!r}"
            )
        _validate_twist_ordinal(self.twist_ordinal)
        phase = _as_fraction(self.phase, "phase")
        magnitude = _as_fraction(self.magnitude, "magnitude")
        confidence = (
            None
            if self.confidence is None
            else _as_fraction(self.confidence, "confidence")
        )
        object.__setattr__(self, "phase", phase)
        object.__setattr__(self, "magnitude", magnitude)
        object.__setattr__(self, "confidence", confidence)
        if not (Fraction(0) <= phase < Fraction(1)):
            raise ValueError(f"phase must be in [0, 1), got {phase!r}")
        if self.face not in (-1, 1):
            raise ValueError(f"face must be -1 or +1, got {self.face!r}")
        if self.sign not in (-1, 0, 1):
            raise ValueError(f"sign must be -1, 0, or +1, got {self.sign!r}")
        _validate_unit_interval(magnitude, "magnitude")
        if self.gauge not in VALID_GAUGE_KINDS:
            raise ValueError(f"unknown gauge kind: {self.gauge!r}")
        if self.grain not in GRAIN_ORDER:
            raise ValueError(f"unknown grain: {self.grain!r}")
        if confidence is not None:
            _validate_unit_interval(confidence, "confidence")

    @property
    def axis_state(self) -> AxisState:
        """Return the directional projection ``state_A(W) = (sign, magnitude)``."""

        return AxisState(sign=self.sign, magnitude=self.magnitude)


# Handoff naming parity: MetricPoint is the wire-name in the v3 sketch.
# Internally we treat MetricPoint and MetricDiskState as the same record.
MetricPoint = MetricDiskState


def make_metric_disk_state(
    *,
    axis: MetricAxis,
    grain: Grain,
    twist_ordinal: int = 0,
    phase: Fraction = Fraction(0),
    face: Face | None = None,
    sign: AxisSign = 0,
    magnitude: Fraction = Fraction(0),
    gauge: GaugeKind = "radius",
    confidence: Fraction | None = None,
) -> MetricDiskState:
    """Build a ``MetricDiskState`` with derived prime and optional face.

    The direct dataclass remains available for wire-format round-tripping.
    New code should prefer this helper so primitive axes cannot accidentally
    alias to the wrong prime anchor.
    """

    if face is None:
        face = mobius_face_for_twist(twist_ordinal)
    return MetricDiskState(
        axis=axis,
        prime_axis=prime_for_axis(axis),
        grain=grain,
        twist_ordinal=twist_ordinal,
        phase=phase,
        face=face,
        sign=sign,
        magnitude=magnitude,
        gauge=gauge,
        confidence=confidence,
    )


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
            if s.grain != self.grain:
                raise ValueError(
                    f"state grain {s.grain!r} does not match tensor grain "
                    f"{self.grain!r} for axis {s.axis!r}"
                )
        axes = [s.axis for s in self.states]
        if len(axes) != len(set(axes)):
            raise ValueError("GrainTensor cannot contain duplicate metric axes")

    def state_for_axis(self, axis: MetricAxis) -> MetricDiskState:
        """Return the disk state for ``axis`` or raise ``KeyError``."""

        for state in self.states:
            if state.axis == axis:
                return state
        raise KeyError(f"axis {axis!r} is not present in this grain tensor")
