# core/bridge/bridge_engine.py
# hmmm: observational only. Correlations + divergence flags.

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .math_utils import pearson, l1

OFAMS = ["P","K","Q","T","S"]
BMETS = ["C","R","D","N","L","O","F","E","I"]

def _op_vec(o: Dict[str, Any]) -> List[float]:
    v = o["vector"]
    return [float(v[f]) for f in OFAMS]

def _b_vec(b: Dict[str, Any]) -> List[float]:
    m = b["metrics"]
    return [float(m[k]) for k in BMETS]

def _op_round_vec(
    round_ids: List[str],
    round_lookup: Dict[str, Dict[str, Any]],
    turn_op_lookup: Dict[str, Dict[str, Any]],
) -> List[float]:
    """
    Sum per-turn operator counts across all turns belonging to the given round_ids,
    then renormalize to get a proportional vector aligned to this behavioral window.
    """
    counts = {f: 0 for f in OFAMS}
    b_total = 0
    for rid in round_ids:
        r = round_lookup.get(rid, {})
        for tid in r.get("turn_ids", []):
            op = turn_op_lookup.get(tid)
            if op:
                for f in OFAMS:
                    counts[f] += op["counts"].get(f, 0)
                b_total += op["counts"].get("B_total", 0)
    if b_total <= 0:
        return [0.0] * len(OFAMS)
    return [counts[f] / b_total for f in OFAMS]

def compute_bridge_windows(
    *,
    rounds: List[Dict[str, Any]],
    turns: List[Dict[str, Any]],
    operator_outputs: List[Dict[str, Any]],
    per_turn_operator_outputs: List[Dict[str, Any]],
    behavioral_outputs: List[Dict[str, Any]],
    divergence_threshold: float = 0.20,
    closed_rounds_only: bool = True,
) -> List[Dict[str, Any]]:
    # Build lookups for round-aligned operator computation
    round_lookup: Dict[str, Dict[str, Any]] = {r["round_id"]: r for r in rounds}
    # per_turn_operator_outputs use window_ids[0] as the turn_id key
    turn_op_lookup: Dict[str, Dict[str, Any]] = {
        o["window_ids"][0]: o for o in per_turn_operator_outputs
    }

    # Precompute round-aligned operator vectors for each behavioral window
    round_op_vecs = [
        _op_round_vec(b["round_ids"], round_lookup, turn_op_lookup)
        for b in behavioral_outputs
    ]

    outs: List[Dict[str, Any]] = []
    prev_o: Optional[List[float]] = None
    prev_b: Optional[List[float]] = None

    for i, b in enumerate(behavioral_outputs):
        ovec = round_op_vecs[i]
        bvec = _b_vec(b)

        # Correlations across the bridge window are underpowered in v1 (n observations small),
        # so we compute correlation across time using accumulated history up to i.
        # Deterministic and simple.
        corr_items = []
        for fi, f in enumerate(OFAMS):
            xs = [round_op_vecs[j][fi] for j in range(i+1)]
            for mi, m in enumerate(BMETS):
                ys = [_b_vec(behavioral_outputs[j])[mi] for j in range(i+1)]
                if len(xs) >= 2:
                    val = pearson(xs, ys)
                    corr_items.append({
                        "operator_family": f,
                        "behavioral_metric": m,
                        "method": "pearson",
                        "value": val,
                        "n": len(xs)
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
                        "thresholds_used": {"divergence_threshold": divergence_threshold}
                    }
                })
                flags.append({"level":"warn","code":"inspect_window","message":"Operator shifted without behavioral change; inspect tokenization/bones window."})

            elif dB >= divergence_threshold and dO < divergence_threshold:
                divergences.append({
                    "round_id": b["round_ids"][-1],
                    "type": "B_spike_without_O",
                    "details": {
                        "summary": "Behavioral spike exceeded threshold without Operator shift.",
                        "operator_delta_L1": dO,
                        "behavioral_delta_L1": dB,
                        "thresholds_used": {"divergence_threshold": divergence_threshold}
                    }
                })
                flags.append({"level":"warn","code":"inspect_window","message":"Behavioral spiked without operator shift; inspect marker hits / constraint proxy."})

            elif dB >= divergence_threshold and dO >= divergence_threshold:
                divergences.append({
                    "round_id": b["round_ids"][-1],
                    "type": "both_shift_unexpectedly",
                    "details": {
                        "summary": "Both Operator and Behavioral shifted beyond threshold.",
                        "operator_delta_L1": dO,
                        "behavioral_delta_L1": dB,
                        "thresholds_used": {"divergence_threshold": divergence_threshold}
                    }
                })
                flags.append({"level":"info","code":"inspect_window","message":"Both layers shifted; likely genuine interaction change."})

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
                "exclude_open_rounds": True
            },
            "hmm": {
                "contained": ["Bridge uses thresholded L1 divergence and Pearson correlations.",
                              "Operator vectors aligned to behavioral round_ids via per-turn sum."],
                "deferred": ["Statistical significance / p-values.", "Alt correlation methods."]
            }
        })

    return outs
