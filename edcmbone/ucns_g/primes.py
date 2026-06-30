# ratios: loc_comments=32:37 imports_exports=3:1 calls_definitions=3:1
"""
edcmbone.ucns_g.primes
~~~~~~~~~~~~~~~~~~~~~~

Prime-axis assignment for UCNS-G v3.

From the v3 handoff (canonical audit projection):

    Operator (PKQTS) primitive axes:
        P → 2
        K → 3
        Q → 5
        T → 7
        S → 11

    EDCM behavioral primitive axes:
        C → 13
        R → 17
        D → 19
        N → 23
        L → 29
        O → 31
        F → 37
        E → 41
        I → 43

Rule:
    primitive metric axes sit on prime anchors.
    composite positions may represent interactions/couplings.

All anchor primes are members of the PCNA topology v1 node set
(first 53 primes); see ``canon_eng/pcna_topology_v1.md``.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping, Tuple


# Operator-layer primitive metric axes (PKQTS).
PRIMITIVE_OPERATOR_AXES: Tuple[str, ...] = ("P", "K", "Q", "T", "S")

# EDCM behavioral primitive metric axes.
PRIMITIVE_METRIC_AXES: Tuple[str, ...] = (
    "C", "R", "D", "N", "L", "O", "F", "E", "I",
)

# Frozen prime-axis assignment table.
_RAW_ASSIGNMENT: Mapping[str, int] = {
    # Operator layer
    "P": 2,
    "K": 3,
    "Q": 5,
    "T": 7,
    "S": 11,
    # EDCM behavioral layer
    "C": 13,
    "R": 17,
    "D": 19,
    "N": 23,
    "L": 29,
    "O": 31,
    "F": 37,
    "E": 41,
    "I": 43,
}

PRIME_AXIS_ASSIGNMENT: Mapping[str, int] = MappingProxyType(dict(_RAW_ASSIGNMENT))


def prime_for_axis(axis: str) -> int:
    """Return the canonical anchor prime for a primitive metric axis.

    Raises ``KeyError`` if ``axis`` is not a primitive axis. Composite /
    interaction positions are intentionally not in this table — those
    belong to a separate coupling layer (see v3 handoff §13 open items).
    """
    try:
        return PRIME_AXIS_ASSIGNMENT[axis]
    except KeyError as exc:
        raise KeyError(
            f"{axis!r} is not a primitive UCNS-G axis; "
            f"valid axes: {sorted(PRIME_AXIS_ASSIGNMENT)}"
        ) from exc
# ratios: loc_comments=32:37 imports_exports=3:1 calls_definitions=3:1
