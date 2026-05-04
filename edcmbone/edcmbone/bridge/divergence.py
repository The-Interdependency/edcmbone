"""
Bridge-layer divergence flags.
Threshold-based: correlation < threshold ⇒ layer pair flagged as divergent.

Divergence is a diagnostic signal (lensing-as-structure principle) — not an error.
Low cross-layer correlation means the two layers are reading different structure
in the same transcript. That disagreement carries information beyond either reading.
"""
from __future__ import annotations
from typing import NamedTuple
from .correlate import BridgeCorrelations

DEFAULT_THRESHOLD: float = 0.2


class DivergenceFlags(NamedTuple):
    """Per-pair divergence flags. True = corr < threshold = diagnostic signal."""
    OB_divergent: bool  # Operator ↔ Behavioral
    OC_divergent: bool  # Operator ↔ Content
    BC_divergent: bool  # Behavioral ↔ Content


def flag_divergence(
    correlations: BridgeCorrelations,
    threshold: float = DEFAULT_THRESHOLD,
) -> DivergenceFlags:
    """
    Flag layer pairs as divergent when |correlation| is below threshold.
    Absolute value used: strong negative correlation is still strong correlation.
    """
    return DivergenceFlags(
        OB_divergent=abs(correlations.OB) < threshold,
        OC_divergent=abs(correlations.OC) < threshold,
        BC_divergent=abs(correlations.BC) < threshold,
    )
