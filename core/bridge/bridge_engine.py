# ratios: loc_comments=181:24 imports_exports=4:1 calls_definitions=35:4
# core/bridge/bridge_engine.py
# hmmm: observational only. Correlations + divergence flags.

from __future__ import annotations

import math
from typing import Any, Dict, List, Optional

from .math_utils import l1

OFAMS = ["P", "K", "Q", "T", "S"]
BMETS = ["C", "R", "D", "N", "L", "O", "F", "E", "I"]


def _b_vec(b: Dict[str, Any]) -> List[float]:
    m = b["metrics"]
    return [float(m[k]) for k in BMETS]


def _aggregate_op_vec_for_rounds(
    round_ids: List[str],
    rounds: List[Dict[str, Any]],
    turn_op_map: Dict[str, Dict[str, Any]],
) -> List[float]:
    """Sum per-turn operator counts for all turns in the given rounds, then renormalize."""
    r_lookup = {r["round_id"]: r for r in rounds}
    agg = {f: 0 for f in OFAMS}
    total = 0
    for rid in round_ids:
        r = r_lookup.get(rid)
        if not r:
            continue
        for tid in r.get("turn_ids", []):
            op = turn_op_map.get(tid)
            if not op:
                continue
            counts = op["counts"]
            bt = int(counts.get("B_total", 0))
            total += bt
            for f in OFAMS:
                agg[f] += int(counts.get(f, 0))
    if total <= 0:
        return [0.0] * len(OFAMS)
    return [agg[f] / total for f in OFAMS]


def _pearson_from_accumulators(
    n: int,
    S_xx: float,
    S_yy: float,
    S_xy: float,
) -> float:
    """Compute Pearson r from Welford online accumulators in O(1).

    S_xx, S_yy, S_xy are sum-of-squared-deviations from running means,
    accumulated via Welford's algorithm to avoid catastrophic cancellation.
    """
    if n < 2:
        return 0.0
    den = math.sqrt(max(0.0, S_xx * S_yy))
    if den == 0.0:
        return 0.0
    return max(-1.0, min(1.0, S_xy / den))


def compute_bridge_windows(
    *,
    rounds: List[Dict[str, Any]],
    turns: List[Dict[str, Any]],
    operator_outputs: List[Dict[str, Any]],
    behavioral_outputs: List[Dict[str, Any]],
    per_turn_operator: Optional[List[Dict[str, Any]]] = None,
    divergence_threshold: float = 0.20,
    closed_rounds_only: bool = True,
) -> List[Dict[str, Any]]:
    """
    Align bridge windows by behavioral window round_ids.

    When per_turn_operator is supplied (preferred), the operator vector for each
    bridge window is computed by summing per-turn operator counts for every turn
    that belongs to the rounds in that behavioral window, then renormalizing.
    This avoids the mismatch between turn-windows and round-windows.

    Falls back to index-based alignment when per_turn_operator is None.

    Pearson correlations are computed via Welford's online algorithm: each
    accumulator stores [n, mean_x, mean_y, S_xx, S_yy, S_xy] where S_xx/yy/xy
    are sum-of-squared-deviations from running means, giving O(n) overall
    complexity with numerical stability for near-constant windows.
    """
    n = len(behavioral_outputs)
    outs: List[Dict[str, Any]] = []

    if per_turn_operator is not None:
        turn_op_map = {o["window_ids"][0]: o for o in per_turn_operator}
        aligned_op_vecs = [
            _aggregate_op_vec_for_rounds(b["round_ids"], rounds, turn_op_map)
            for b in behavioral_outputs
        ]
    else:
        n = min(n, len(operator_outputs))

        def _op_vec(o: Dict[str, Any]) -> List[float]:
            v = o["vector"]
            return [float(v[f]) for f in OFAMS]

        aligned_op_vecs = [_op_vec(operator_outputs[i]) for i in range(n)]

    # Welford online accumulators for Pearson, indexed by (fi, mi).
    # Each entry: [n (int), mean_x, mean_y, S_xx, S_yy, S_xy]
    # where S_xx = Σ(x_i - μ_x)^2, etc., accumulated via Welford's update.
    acc: Dict[tuple, List] = {
        (fi, mi): [0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for fi in range(len(OFAMS))
        for mi in range(len(BMETS))
    }

    prev_o: Optional[List[float]] = None
    prev_b: Optional[List[float]] = None

    for i in range(n):
        b = behavioral_outputs[i]
        ovec = aligned_op_vecs[i]
        bvec = _b_vec(b)

        # Welford update: O(|families|·|metrics|) per window
        for fi in range(len(OFAMS)):
            x = ovec[fi]
            for mi in range(len(BMETS)):
                y = bvec[mi]
                a = acc[(fi, mi)]
                n_new = a[0] + 1
                dx = x - a[1]            # deviation from old mean_x
                a[1] += dx / n_new       # update mean_x
                dy = y - a[2]            # deviation from old mean_y
                a[2] += dy / n_new       # update mean_y
                a[3] += dx * (x - a[1]) # S_xx: dx * (x - new mean_x)
                a[4] += dy * (y - a[2]) # S_yy: dy * (y - new mean_y)
                a[5] += dx * (y - a[2]) # S_xy: dx * (y - new mean_y)
                a[0] = n_new

        # Compute Pearson correlations from Welford accumulators
        corr_items = []
        for fi, f in enumerate(OFAMS):
            for mi, m_key in enumerate(BMETS):
                a = acc[(fi, mi)]
                n_acc = a[0]
                if n_acc >= 2:
                    val = _pearson_from_accumulators(
                        n_acc, a[3], a[4], a[5]
                    )
                    corr_items.append({
                        "operator_family": f,
                        "behavioral_metric": m_key,
                        "method": "pearson",
                        "value": val,
                        "n": n_acc,
                    })

        divergences = []
        flags = []

        if prev_o is not None and prev_b is not None:
            dO = l1(ovec, prev_o)
            dB = l1(bvec, prev_b)

            if dO >= divergence_threshold and dB < divergence_threshold:
                divergences.append({
                    "round_id": b["round_ids"][-1],
                    "type": "O_shift_without_B",
                    "details": {
                        "summary": "Operator shift exceeded threshold without Behavioral shift.",
                        "operator_delta_L1": dO,
                        "behavioral_delta_L1": dB,
                        "thresholds_used": {"divergence_threshold": divergence_threshold},
                    },
                })
                flags.append({"level": "warn", "code": "inspect_window",
                              "message": "Operator shifted without behavioral change; inspect tokenization/bones window."})

            elif dB >= divergence_threshold and dO < divergence_threshold:
                divergences.append({
                    "round_id": b["round_ids"][-1],
                    "type": "B_spike_without_O",
                    "details": {
                        "summary": "Behavioral spike exceeded threshold without Operator shift.",
                        "operator_delta_L1": dO,
                        "behavioral_delta_L1": dB,
                        "thresholds_used": {"divergence_threshold": divergence_threshold},
                    },
                })
                flags.append({"level": "warn", "code": "inspect_window",
                              "message": "Behavioral spiked without operator shift; inspect marker hits / constraint proxy."})

            elif dB >= divergence_threshold and dO >= divergence_threshold:
                divergences.append({
                    "round_id": b["round_ids"][-1],
                    "type": "both_shift_unexpectedly",
                    "details": {
                        "summary": "Both Operator and Behavioral shifted beyond threshold.",
                        "operator_delta_L1": dO,
                        "behavioral_delta_L1": dB,
                        "thresholds_used": {"divergence_threshold": divergence_threshold},
                    },
                })
                flags.append({"level": "info", "code": "inspect_window",
                              "message": "Both layers shifted; likely genuine interaction change."})

        prev_o = ovec
        prev_b = bvec

        outs.append({
            "schema_id": "edcmbone/bridge_output_v1",
            "version": "1.0.0",
            "attribution": "GPT generated; context, prompt Erin Spencer",
            "window_id": f"bridge_window::{i}",
            "round_ids": b["round_ids"],
            "closed_rounds_only": True,
            "correlations": corr_items,
            "divergences": divergences,
            "flags": flags,
            "rules_frozen": {
                "bridge_is_read_only": True,
                "does_not_modify_O_or_B": True,
                "operator_alignment_method": "sum_and_renormalize",
                "exclude_open_rounds": True,
            },
            "hmmm": {
                "contained": [
                    "Bridge uses thresholded L1 divergence and Pearson correlations.",
                    "Operator vectors aligned by behavioral window round_ids via per-turn aggregation.",
                ],
                "deferred": ["Statistical significance / p-values.", "Alt correlation methods."],
            },
        })

    return outs
# ratios: loc_comments=181:24 imports_exports=4:1 calls_definitions=35:4
