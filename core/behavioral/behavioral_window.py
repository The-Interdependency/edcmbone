# core/behavioral/behavioral_window.py
# hmmm: rolling windows over CLOSED rounds only by default.

from __future__ import annotations

from typing import Any, Dict, List

from .behavioral_metrics import compute_behavioral_for_window

def compute_behavioral_windows(
    *,
    rounds: List[Dict[str, Any]],
    turns: List[Dict[str, Any]],
    markers_inventory: Dict[str, Any],
    m_rounds: int = 4,
    stride: int = 1,
    closed_rounds_only: bool = True,
) -> List[Dict[str, Any]]:
    usable = [r for r in rounds if (r.get("status") == "closed") or (not closed_rounds_only)]
    outputs: List[Dict[str, Any]] = []

    prev_feat = None
    prev_intensity = None

    for start in range(0, len(usable), stride):
        win = usable[start:start+m_rounds]
        if not win:
            continue
        rid = [r["round_id"] for r in win]
        out, prev_feat, prev_intensity = compute_behavioral_for_window(
            window_id=f"round_window::{start}:{start+len(win)-1}",
            round_ids=rid,
            rounds=usable,
            turns=turns,
            markers_inventory=markers_inventory,
            prev_window_feature_vec=prev_feat,
            prev_intensity=prev_intensity,
        )
        out["is_partial"] = len(win) < m_rounds
        outputs.append(out)

    return outputs
