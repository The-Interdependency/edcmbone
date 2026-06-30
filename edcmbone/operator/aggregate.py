# ratios: loc_comments=22:24 imports_exports=2:2 calls_definitions=8:2
# === MODULE_BUILD ===
# id: operator_vector_aggregate
#   module_name: operator aggregate
#   module_kind: engine
#   summary: normalizes operator family counts into a stable 5D unit-sum vector.
#   owner: edcmbone-maintainers
#   public_surface: aggregate,OperatorVector
#   internal_surface: FAMILIES
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_backend.py
#   rollout: default_enabled
#   rollback: route callers back to raw counts
# === END MODULE_BUILD ===
"""
Operator-layer 5D vector assembly.
Implements Sigma_f O_f = 1 (frozen v1 conservation constraint).
Zero external dependencies; stdlib only.
"""
from __future__ import annotations
from typing import NamedTuple

FAMILIES: tuple[str, ...] = ("P", "K", "Q", "T", "S")


class OperatorVector(NamedTuple):
    """5D normalized operator vector. Sum = 1.0 when total > 0."""
    P: float
    K: float
    Q: float
    T: float
    S: float
    total: int  # raw bone count; not part of the 5D


def aggregate(counts: dict[str, int]) -> OperatorVector:
    """Normalize family counts to unit-sum fractions (Sigma_f O_f = 1)."""
    total = sum(counts.get(f, 0) for f in FAMILIES)
    if total == 0:
        return OperatorVector(P=0.0, K=0.0, Q=0.0, T=0.0, S=0.0, total=0)
    return OperatorVector(
        P=counts.get("P", 0) / total,
        K=counts.get("K", 0) / total,
        Q=counts.get("Q", 0) / total,
        T=counts.get("T", 0) / total,
        S=counts.get("S", 0) / total,
        total=total,
    )
# ratios: loc_comments=22:24 imports_exports=2:2 calls_definitions=8:2
