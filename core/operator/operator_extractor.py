# core/operator/operator_extractor.py
# hmmm: computes operator outputs over rolling k-turn windows.

from __future__ import annotations

from typing import Any, Dict, List

from .inventories import load_affixes, load_bones_map
from .matcher import (
    contraction_split, match_whole_word, match_punct,
    hyphen_compound_emission, match_affixes, choose_family
)

def _empty_counts() -> Dict[str, int]:
    return {"B_total": 0, "P": 0, "K": 0, "Q": 0, "T": 0, "S": 0}

def _vector_from_counts(c: Dict[str, int]) -> Dict[str, float]:
    total = c["B_total"]
    if total <= 0:
        return {"P": 0.0, "K": 0.0, "Q": 0.0, "T": 0.0, "S": 0.0, "sum": 0.0}
    v = {f: c[f] / total for f in ["P", "K", "Q", "T", "S"]}
    v["sum"] = sum(v[f] for f in ["P","K","Q","T","S"])
    return v

def _process_turn_tokens(
    turn: Dict[str, Any],
    bones_map: Dict[str, str],
    pref_map: Dict[str, str],
    suf_map: Dict[str, str],
) -> Dict[str, Any]:
    """Core per-turn operator computation. Accepts pre-built maps (no repeated loading)."""
    counts = _empty_counts()
    audit = {"matched_free_bones": 0, "matched_affixes": 0, "matched_punct": 0, "excluded_tokens": 0}

    for surf in turn.get("tokens_surface", []):
        # punctuation emissions
        punct_fams = match_punct(surf)
        if punct_fams:
            fam = choose_family(punct_fams)
            counts[fam] += 1
            counts["B_total"] += 1
            audit["matched_punct"] += 1
            continue

        # hyphen compound emits one K (in addition to internal free bones processed normally)
        if "-" in surf:
            # emit one K
            counts["K"] += 1
            counts["B_total"] += 1
            audit["matched_punct"] += 1  # treat as connective emission
            # then continue processing internal parts as separate surface tokens for closed-class only
            parts = surf.split("-")
            for p in parts:
                for sub in contraction_split(p):
                    fams = match_whole_word(sub, bones_map)
                    if fams:
                        fam = choose_family(fams)
                        counts[fam] += 1
                        counts["B_total"] += 1
                        audit["matched_free_bones"] += 1
                    else:
                        audit["excluded_tokens"] += 1
            continue

        # contractions split
        subs = contraction_split(surf)
        for sub in subs:
            # whole-word precedence
            fams = match_whole_word(sub, bones_map)
            if fams:
                fam = choose_family(fams)
                counts[fam] += 1
                counts["B_total"] += 1
                audit["matched_free_bones"] += 1
                continue

            # affixes only if no whole-word match
            aff_fams, _root = match_affixes(sub, pref_map, suf_map)
            if aff_fams:
                for af in aff_fams:
                    fam = choose_family([af])
                    counts[fam] += 1
                    counts["B_total"] += 1
                    audit["matched_affixes"] += 1
            else:
                audit["excluded_tokens"] += 1

    return {
        "schema_id": "edcmbone/operator_output_v1",
        "version": "1.0.0",
        "attribution": "GPT generated; context, prompt Erin Spencer",
        "operator_families_option": "A",
        "window_id": f"turn::{turn['turn_id']}",
        "window_unit": "turn",
        "window_ids": [turn["turn_id"]],
        "is_partial": False,
        "counts": {
            **counts,
            "audit": audit
        },
        "vector": _vector_from_counts(counts),
        "rules_frozen": {
            "lowercase_before_match": True,
            "contractions_split": True,
            "hyphen_compound_emits_one_K": True,
            "question_mark_emits_one_Q": True,
            "em_dash_emits_zero": True,
            "slash_ignored_v1": True,
            "collision_priority": ["P", "K", "Q", "T", "S"],
            "aggregation_method": "sum_and_renormalize"
        },
        "hmm": {
            "contained": ["Whole-word precedence over affix stripping."],
            "deferred": ["Slash-as-K decision.", "Expanded contraction map."]
        }
    }


def compute_operator_for_turn(
    turn: Dict[str, Any],
    bones_inventory: Dict[str, Any],
    affixes_inventory: Dict[str, Any],
) -> Dict[str, Any]:
    """Public single-turn API. Builds maps from raw inventories (use batch APIs for loops)."""
    bones_map = load_bones_map(bones_inventory)
    pref_map, suf_map = load_affixes(affixes_inventory)
    return _process_turn_tokens(turn, bones_map, pref_map, suf_map)


def compute_per_turn_operator(
    *,
    turns: List[Dict[str, Any]],
    bones_inventory: Dict[str, Any],
    affixes_inventory: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """Per-turn operator outputs (one entry per turn, indexed by turn_id). Maps built once."""
    bones_map = load_bones_map(bones_inventory)
    pref_map, suf_map = load_affixes(affixes_inventory)
    return [_process_turn_tokens(t, bones_map, pref_map, suf_map) for t in turns]


def _sum_counts(operator_turn_outputs: List[Dict[str, Any]]) -> Dict[str, int]:
    c = _empty_counts()
    audit = {"matched_free_bones": 0, "matched_affixes": 0, "matched_punct": 0, "excluded_tokens": 0}
    for o in operator_turn_outputs:
        oc = o["counts"]
        c["B_total"] += int(oc["B_total"])
        for f in ["P","K","Q","T","S"]:
            c[f] += int(oc[f])
        a = oc["audit"]
        for k in audit:
            audit[k] += int(a.get(k, 0))
    c["audit"] = audit  # type: ignore
    return c


def compute_operator_windows(
    *,
    turns: List[Dict[str, Any]],
    bones_inventory: Dict[str, Any],
    affixes_inventory: Dict[str, Any],
    k_turns: int = 8,
    stride: int = 1
) -> List[Dict[str, Any]]:
    # build maps once for the entire batch
    bones_map = load_bones_map(bones_inventory)
    pref_map, suf_map = load_affixes(affixes_inventory)

    per_turn = [_process_turn_tokens(t, bones_map, pref_map, suf_map) for t in turns]

    outputs: List[Dict[str, Any]] = []
    if not per_turn:
        return outputs

    for start in range(0, len(per_turn), stride):
        win = per_turn[start:start+k_turns]
        if not win:
            continue
        counts = _sum_counts(win)
        audit = counts.pop("audit")  # type: ignore
        counts["audit"] = audit  # type: ignore
        out = {
            "schema_id": "edcmbone/operator_output_v1",
            "version": "1.0.0",
            "attribution": "GPT generated; context, prompt Erin Spencer",
            "operator_families_option": "A",
            "window_id": f"turn_window::{start}:{start+len(win)-1}",
            "window_unit": "turn",
            "window_ids": [o["window_ids"][0] for o in win],
            "is_partial": len(win) < k_turns,
            "counts": counts,
            "vector": _vector_from_counts(counts),
            "rules_frozen": win[0]["rules_frozen"],
            "hmm": {
                "contained": ["Sum-and-renormalize aggregation."],
                "deferred": ["Alternative aggregation (mean of turn vectors)."]
            }
        }
        outputs.append(out)

    return outputs
