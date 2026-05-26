"""EDCM / UCNS metric orthogonality primitives.

Implements the v0.2 signed-axis model for metric identity and state transport.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

SIGNED_TERNARY = (-1, 0, 1)


@dataclass(frozen=True)
class AxisState:
    """Signed ternary axis state.

    NA is represented by ``enabled=False`` with ``s`` and ``m`` left as ``None``.
    When enabled, ``s`` must be in {-1,0,+1} and ``m`` in [0,1].
    """

    enabled: bool
    s: Optional[int] = None
    m: Optional[float] = None

    def __post_init__(self) -> None:
        if not self.enabled:
            if self.s is not None or self.m is not None:
                raise ValueError("disabled (NA) axis state must not carry s or m")
            return
        if self.s not in SIGNED_TERNARY:
            raise ValueError("s must be one of -1, 0, +1")
        if self.m is None or not (0.0 <= float(self.m) <= 1.0):
            raise ValueError("m must be in [0,1]")

    @classmethod
    def na(cls) -> "AxisState":
        return cls(enabled=False)


@dataclass(frozen=True)
class MetricAxis:
    metric_id: str
    axis_name: str
    parent_object: str
    primitive: bool = True


def canonical_axes() -> dict[str, MetricAxis]:
    """Return canonical metric axis registry for orthogonality checks."""
    axes = {
        "edcm.behavioral.C.constraint_strain": MetricAxis("edcm.behavioral.C.constraint_strain", "constraint strain", "ConstraintField / evidence"),
        "edcm.behavioral.R.refusal_density": MetricAxis("edcm.behavioral.R.refusal_density", "refusal / resistance contact", "ConstraintField / Contact"),
        "edcm.behavioral.D.deflection": MetricAxis("edcm.behavioral.D.deflection", "deflection / return", "ConstraintField / Contact"),
        "edcm.behavioral.I.integration": MetricAxis("edcm.behavioral.I.integration", "integration / dis-integration", "ConstraintField / Resolution"),
        "edcm.behavioral.F.fixation": MetricAxis("edcm.behavioral.F.fixation", "recurrence / release", "FieldMotion"),
        "edcm.behavioral.E.escalation": MetricAxis("edcm.behavioral.E.escalation", "escalation / de-escalation", "FieldMotion"),
        "edcm.behavioral.O_scope": MetricAxis("edcm.behavioral.O_scope", "expansion / contraction", "FieldMotion"),
        "edcm.behavioral.O_confidence": MetricAxis("edcm.behavioral.O_confidence", "confidence polarity", "confidence evidence"),
        "edcm.behavioral.L_load": MetricAxis("edcm.behavioral.L_load", "load increase / decrease", "ConstraintField"),
        "edcm.behavioral.L_loss": MetricAxis("edcm.behavioral.L_loss", "coherence loss / recovery", "continuity evidence"),
        "edcm.behavioral.L_resistance": MetricAxis("edcm.behavioral.L_resistance", "resistance hardening / softening", "ConstraintField / Contact"),
        "edcm.behavioral.N.noise": MetricAxis("edcm.behavioral.N.noise", "signal efficiency / inefficiency", "system evidence"),
        "edcm.round.P_progress": MetricAxis("edcm.round.P_progress", "progress / regression", "sequence state"),
        "edcm.state.kappa": MetricAxis("edcm.state.kappa", "stored tension / release", "state composite"),
        "edcm.projection.CM": MetricAxis("edcm.projection.CM", "projection over C and I", "projection", primitive=False),
    }
    return axes
