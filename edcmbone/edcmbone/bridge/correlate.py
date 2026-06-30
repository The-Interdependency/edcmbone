# ratios: loc_comments=43:17 imports_exports=5:2 calls_definitions=14:6
"""
Bridge-layer cross-layer correlations (ternary: O↔B, O↔C, B↔C).
Bridge is read-only — never modifies any layer. (Canon v1 rule, carried forward.)

All three layer pairs produce independent Pearson correlations over a window
of per-round summary scalars. Disagreement between layer readings is itself
a diagnostic signal (lensing-as-structure principle).
"""
from __future__ import annotations
from typing import NamedTuple, Sequence

from ..operator.aggregate import OperatorVector
from ..behavioral.snapshot.metrics import BehavioralSnapshot
from ..content.vector import ContentVector


def _pearson(xs: list[float], ys: list[float]) -> float:
    """Pearson correlation. Returns 0.0 if undefined (< 2 points or zero variance)."""
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = (sum((x - mx) ** 2 for x in xs) / n) ** 0.5
    sy = (sum((y - my) ** 2 for y in ys) / n) ** 0.5
    if sx == 0.0 or sy == 0.0:
        return 0.0
    return num / (n * sx * sy)


def _op_scalar(v: OperatorVector) -> float:
    """Structural density proxy: P+K share captures connectivity."""
    return v.P + v.K


def _beh_scalar(v: BehavioralSnapshot) -> float:
    """Behavioral summary: constraint load L as primary coupling axis."""
    return v.L


def _content_scalar(v: ContentVector) -> float:
    """Content summary: mean scalar rating."""
    r = v.ratings
    return (r.utility + r.clarity + r.focus + r.aesthetic + r.psychological + r.epistemic) / 6.0


class BridgeCorrelations(NamedTuple):
    """Ternary cross-layer correlations. All values in [-1, 1]."""
    OB: float  # Operator ↔ Behavioral
    OC: float  # Operator ↔ Content
    BC: float  # Behavioral ↔ Content


def correlate(
    op_window: Sequence[OperatorVector],
    beh_window: Sequence[BehavioralSnapshot],
    content_window: Sequence[ContentVector],
) -> BridgeCorrelations:
    """
    Compute ternary correlations over a matched window of per-round vectors.
    All three sequences must have the same length (one entry per round).
    Mismatched lengths return 0.0 correlations.
    """
    n = min(len(op_window), len(beh_window), len(content_window))
    if n < 2:
        return BridgeCorrelations(OB=0.0, OC=0.0, BC=0.0)
    ops = [_op_scalar(v) for v in op_window[:n]]
    behs = [_beh_scalar(v) for v in beh_window[:n]]
    cons = [_content_scalar(v) for v in content_window[:n]]
    return BridgeCorrelations(
        OB=_pearson(ops, behs),
        OC=_pearson(ops, cons),
        BC=_pearson(behs, cons),
    )
# ratios: loc_comments=43:17 imports_exports=5:2 calls_definitions=14:6
