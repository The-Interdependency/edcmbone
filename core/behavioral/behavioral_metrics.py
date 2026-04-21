# core/behavioral/behavioral_metrics.py
# hmmm: implements behavioral_formulas_v1.md deterministically.

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple
from math import sqrt

from core.parsing.normalizer import normalize_text_for_matching
from .marker_matcher import Hit, match_phrases_in_turn_tokens
from .structural_proxies import (
    constraint_statement_proxy_count,
    total_tokens_in_turn_ids,
    count_question_marks,
)

def sat(x: float, cap: float) -> float:
    if cap <= 0:
        return 1.0 if x > 0 else 0.0
    return min(1.0, x / cap)

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

def cosine(v: List[float], w: List[float]) -> float:
    dot = sum(a*b for a, b in zip(v, w))
    nv = sqrt(sum(a*a for a in v))
    nw = sqrt(sum(b*b for b in w))
    if nv == 0 or nw == 0:
        return 0.0
    return clamp01(dot / (nv * nw))

def _pack_hits(hits: List[Hit]) -> Dict[str, Any]:
    return {
        "count": len(hits),
        "hits": [
            {
                "tier": h.tier,
                "marker_id": h.marker_id,
                "weight": h.weight,
                "matched_text": h.matched_text,
                "span": {"turn_id": h.turn_id, "start_token": h.start_token, "end_token": h.end_token},
            }
            for h in hits
        ],
    }

def compute_behavioral_for_window(
    *,
    window_id: str,
    round_ids: List[str],
    rounds: List[Dict[str, Any]],
    turns: List[Dict[str, Any]],
    markers_inventory: Dict[str, Any],
    prev_window_feature_vec: Optional[List[float]],
    prev_intensity: Optional[float],
) -> Tuple[Dict[str, Any], List[float], float]:
    # collect turn_ids in window
    r_lookup = {r["round_id"]: r for r in rounds}
    turn_ids: List[str] = []
    for rid in round_ids:
        rr = r_lookup.get(rid)
        if rr:
            turn_ids.extend(rr.get("turn_ids", []))

    t_lookup = {t["turn_id"]: t for t in turns}

    mm = markers_inventory.get("metric_marker_sets", {})

    # Helpers to grab tierA phrase lists with weights
    def _get_phrases(metric: str, key: str) -> List[str]:
        return (mm.get(metric, {}).get("tier_a_structural", {}) or {}).get(key, []) or []

    def _get_weight(metric: str, key: str, default: float) -> float:
        # weights may exist under "weights" or not; we keep deterministic defaults
        weights = (mm.get(metric, {}).get("tier_a_structural", {}) or {}).get("weights", {}) or {}
        return float(weights.get(key, default))

    # Build hits per metric
    hits_by_metric: Dict[str, List[Hit]] = {k: [] for k in ["C","R","D","N","L","O","F","E","I"]}

    # Turn-level phrase matching for structural lists
    for tid in turn_ids:
        t = t_lookup.get(tid)
        if not t:
            continue
        toks = t.get("tokens_surface", [])

        # R: refusal phrases
        hard = _get_phrases("R_refusal_density", "hard_refusal_phrases")
        soft = _get_phrases("R_refusal_density", "soft_refusal_phrases")
        hits_by_metric["R"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=hard,
            marker_prefix="R.hard", tier="A_structural",
            weight=_get_weight("R_refusal_density", "hard", 1.0)
        )
        hits_by_metric["R"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=soft,
            marker_prefix="R.soft", tier="A_structural",
            weight=_get_weight("R_refusal_density", "soft", 0.5)
        )

        # D: deflection markers
        shift = _get_phrases("D_deflection", "topic_shift_markers")
        meta = _get_phrases("D_deflection", "meta_discourse_markers")
        hits_by_metric["D"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=shift,
            marker_prefix="D.shift", tier="A_structural", weight=0.6
        )
        hits_by_metric["D"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=meta,
            marker_prefix="D.meta", tier="A_structural", weight=0.8
        )

        # N: padding markers + action markers (action counted separately as RA)
        padding = _get_phrases("N_noise", "non_action_padding_markers")
        actions = _get_phrases("N_noise", "resolution_action_markers")
        hits_by_metric["N"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=padding,
            marker_prefix="N.pad", tier="A_structural", weight=0.5
        )
        # actions stored as N hits too, but RA is derived from them
        hits_by_metric["N"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=actions,
            marker_prefix="N.act", tier="A_structural", weight=1.0
        )

        # L: constraint markers
        modals = _get_phrases("L_load", "constraint_modals")
        conds = _get_phrases("L_load", "constraint_conditionals")
        delims = _get_phrases("L_load", "constraint_delimiters")
        hits_by_metric["L"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=modals,
            marker_prefix="L.modal", tier="A_structural", weight=1.0
        )
        hits_by_metric["L"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=conds,
            marker_prefix="L.cond", tier="A_structural", weight=0.6
        )
        hits_by_metric["L"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=delims,
            marker_prefix="L.delim", tier="A_structural", weight=0.6
        )

        # O: expansion markers
        exp = _get_phrases("O_overextension", "expansion_markers")
        hits_by_metric["O"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=exp,
            marker_prefix="O.exp", tier="A_structural", weight=0.6
        )

        # E: intensity markers
        inten = _get_phrases("E_escalation", "intensity_markers")
        hits_by_metric["E"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=inten,
            marker_prefix="E.int", tier="A_structural", weight=1.0
        )

        # I: correction markers (user) and acknowledgement markers (assistant)
        corr_u = _get_phrases("I_integration_failure", "correction_markers_user")
        ack_a = _get_phrases("I_integration_failure", "ack_markers_assistant")
        hits_by_metric["I"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=corr_u,
            marker_prefix="I.corr", tier="A_structural", weight=1.0
        )
        hits_by_metric["I"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=ack_a,
            marker_prefix="I.ack", tier="A_structural", weight=1.0
        )

        # C: strain (structural proxies: negation+contrast, question pressure, modal collision)
        # Use existing lists if present; otherwise rely on L/R/D.
        neg = _get_phrases("C_constraint_strain", "negation_tokens")
        con = _get_phrases("C_constraint_strain", "contrast_connectors")
        cmods = _get_phrases("C_constraint_strain", "counterfactual_modals")
        hits_by_metric["C"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=neg,
            marker_prefix="C.neg", tier="A_structural", weight=0.35
        )
        hits_by_metric["C"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=con,
            marker_prefix="C.con", tier="A_structural", weight=0.35
        )
        hits_by_metric["C"] += match_phrases_in_turn_tokens(
            turn_id=tid, tokens=toks, phrases=cmods,
            marker_prefix="C.mod", tier="A_structural", weight=0.25
        )

    # Shared counts
    CS = constraint_statement_proxy_count(
        turns, turn_ids,
        constraint_modals=_get_phrases("L_load", "constraint_modals"),
        conditionals=_get_phrases("L_load", "constraint_conditionals"),
        delimiters=_get_phrases("L_load", "constraint_delimiters")
    )
    TOK = total_tokens_in_turn_ids(turns, turn_ids)

    # RA from action hits (subset of N hits with marker_id prefix "N.act:")
    RA = sum(1 for h in hits_by_metric["N"] if h.marker_id.startswith("N.act:"))
    PADDING = sum(1 for h in hits_by_metric["N"] if h.marker_id.startswith("N.pad:"))

    # ---- Metric formulas (frozen defaults) ----
    # C
    C_raw = sum(h.weight for h in hits_by_metric["C"])
    # question pressure: multiple ? in window adds
    qcount = count_question_marks(turns, turn_ids)
    if qcount >= 2:
        C_raw += 0.35
    C = sat(C_raw, 3.0)

    # R
    R_hard = sum(1 for h in hits_by_metric["R"] if h.marker_id.startswith("R.hard:"))
    R_soft = sum(1 for h in hits_by_metric["R"] if h.marker_id.startswith("R.soft:"))
    Rw = 1.0 * R_hard + 0.5 * R_soft
    R_den = Rw / CS
    R = sat(R_den, 0.75)

    # D
    D_shift = sum(1 for h in hits_by_metric["D"] if h.marker_id.startswith("D.shift:"))
    D_meta  = sum(1 for h in hits_by_metric["D"] if h.marker_id.startswith("D.meta:"))
    D_qev = 0  # pattern-based; deferred in code v1
    D_raw = 0.6*D_shift + 0.8*D_meta + 1.0*D_qev
    D = sat(D_raw, 3.0)

    # N
    rr = RA / (RA + PADDING + 1.0)
    N_raw = 1.0 - rr
    if PADDING >= 5 and RA == 0:
        N_raw = 1.0
    N = clamp01(N_raw)

    # L
    M = sum(1 for h in hits_by_metric["L"] if h.marker_id.startswith("L.modal:"))
    Cn = sum(1 for h in hits_by_metric["L"] if h.marker_id.startswith("L.cond:"))
    Dl = sum(1 for h in hits_by_metric["L"] if h.marker_id.startswith("L.delim:"))
    Lw = 1.0*M + 0.6*Cn + 0.6*Dl
    L_den = Lw / CS
    L = sat(L_den, 4.0)

    # O
    O_exp = len(hits_by_metric["O"])
    O_list = 0  # list-growth requires user/assistant role parsing; deferred in code v1
    O_raw = 0.6*O_exp + 1.0*O_list
    O = sat(O_raw, 4.0)

    # F (structural cosine proxy vector)
    neg_ct = sum(1 for h in hits_by_metric["C"] if h.marker_id.startswith("C.neg:"))
    con_ct = sum(1 for h in hits_by_metric["C"] if h.marker_id.startswith("C.con:"))
    refusal_total = len(hits_by_metric["R"])
    feature_vec = [float(M), float(refusal_total), float(qcount), float(neg_ct), float(con_ct)]
    if prev_window_feature_vec is None or len(prev_window_feature_vec) != len(feature_vec):
        F = 0.0
    else:
        F = cosine(feature_vec, prev_window_feature_vec)

    # E (positive derivative)
    punct_intensity = 0  # "!!" patterns already tokenized; can be added later
    Iwin = 1.0*len(hits_by_metric["E"]) + 0.5*punct_intensity
    if prev_intensity is None:
        E = 0.0
    else:
        dI = Iwin - prev_intensity
        E = sat(max(0.0, dI), 4.0)

    # I (integration failure proxy)
    U_corr = sum(1 for h in hits_by_metric["I"] if h.marker_id.startswith("I.corr:"))
    A_ack  = sum(1 for h in hits_by_metric["I"] if h.marker_id.startswith("I.ack:"))
    if U_corr == 0:
        I = 0.0
    else:
        if A_ack == 0:
            I = 1.0
        else:
            I = clamp01(1.0 - min(1.0, A_ack / U_corr))

    out = {
        "schema_id": "edcmbone/behavioral_output_v1",
        "version": "1.0.0",
        "attribution": "GPT generated; context, prompt Erin Spencer",
        "window_id": window_id,
        "round_ids": round_ids,
        "closed_rounds_only": True,
        "is_partial": False,
        "metrics": {"C": C, "R": R, "D": D, "N": N, "L": L, "O": O, "F": F, "E": E, "I": I},
        "raw_counts": {
            "CS": CS,
            "TOK": TOK,
            "RA": RA,
            "marker_hits_by_metric": {
                "C": _pack_hits(hits_by_metric["C"]),
                "R": _pack_hits(hits_by_metric["R"]),
                "D": _pack_hits(hits_by_metric["D"]),
                "N": _pack_hits(hits_by_metric["N"]),
                "L": _pack_hits(hits_by_metric["L"]),
                "O": _pack_hits(hits_by_metric["O"]),
                "F": {"count": 0, "hits": []},
                "E": _pack_hits(hits_by_metric["E"]),
                "I": _pack_hits(hits_by_metric["I"]),
            }
        },
        "hmm": {
            "contained": [
                "Structural proxy behavioral metrics (no embeddings).",
                "Closed rounds only."
            ],
            "deferred": [
                "Pattern-based evasion detection (D_qev).",
                "List growth detector (O_list) with user/assistant role separation.",
                "Punctuation intensity (!!) handling."
            ]
        }
    }

    return out, feature_vec, Iwin
