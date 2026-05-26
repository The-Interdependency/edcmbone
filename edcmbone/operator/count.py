# === MODULE_BUILD ===
# id: operator_family_count
#   module_name: operator family count
#   module_kind: service
#   summary: counts P/K/Q/T/S family assignments per turn and across windows.
#   owner: edcmbone-maintainers
#   public_surface: count_families,count_turn,count_window
#   internal_surface: FAMILIES
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_backend.py
#   rollout: default_enabled
#   rollback: remove public counter entrypoints and call sites
# === END MODULE_BUILD ===
"""
Operator-layer bone-family counter.
Counts P/K/Q/T/S tokens from tokenize_turn output.
Zero external dependencies; stdlib only.
"""
from __future__ import annotations
from typing import Iterable, Optional

FAMILIES: tuple[str, ...] = ("P", "K", "Q", "T", "S")


def count_families(
    tokens: Iterable[tuple[str, Optional[str]]],
) -> dict[str, int]:
    """Count bone tokens by family. Open-class (family=None) tokens are excluded."""
    counts: dict[str, int] = {f: 0 for f in FAMILIES}
    for _, fam in tokens:
        if fam in counts:
            counts[fam] += 1
    return counts


# Alias: per-turn is the same operation.
count_turn = count_families


def count_window(
    turn_counts: Iterable[dict[str, int]],
) -> dict[str, int]:
    """
    Aggregate per-turn counts over a window.
    W_turn(k=8) for Operator per canon v1 windowing policy.
    Caller is responsible for supplying the correct window of turns.
    """
    window: dict[str, int] = {f: 0 for f in FAMILIES}
    for tc in turn_counts:
        for f in FAMILIES:
            window[f] += tc.get(f, 0)
    return window
