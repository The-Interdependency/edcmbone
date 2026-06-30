# ratios: loc_comments=70:19 imports_exports=4:2 calls_definitions=19:2
# core/behavioral/ucns_marker_store.py
# Phase 1: UCNSStore-backed marker lookup for algebraic comparison with phrase matching.

from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from ucns_recursive import UCNSStore, recursive_encode
    _UCNS_AVAILABLE = True
except ImportError:
    _UCNS_AVAILABLE = False

from core.parsing.normalizer import normalize_text_for_matching

# Mirror the phrase list layout from behavioral_metrics.py so changes propagate together.
_PHRASE_MAP: List[tuple] = [
    ("R_refusal_density",     "hard_refusal_phrases",       "R.hard"),
    ("R_refusal_density",     "soft_refusal_phrases",       "R.soft"),
    ("D_deflection",          "topic_shift_markers",        "D.shift"),
    ("D_deflection",          "meta_discourse_markers",     "D.meta"),
    ("N_noise",               "non_action_padding_markers", "N.pad"),
    ("N_noise",               "resolution_action_markers",  "N.act"),
    ("L_load",                "constraint_modals",          "L.modal"),
    ("L_load",                "constraint_conditionals",    "L.cond"),
    ("L_load",                "constraint_delimiters",      "L.delim"),
    ("O_overextension",       "expansion_markers",          "O.exp"),
    ("E_escalation",          "intensity_markers",          "E.int"),
    ("I_integration_failure", "correction_markers_user",    "I.corr"),
    ("I_integration_failure", "ack_markers_assistant",      "I.ack"),
    ("C_constraint_strain",   "negation_tokens",            "C.neg"),
    ("C_constraint_strain",   "contrast_connectors",        "C.con"),
    ("C_constraint_strain",   "counterfactual_modals",      "C.mod"),
]

_MAX_PHRASE_TOKENS = 8  # longest phrase we'll ever check windows for


def build_marker_store(markers_inventory: Dict[str, Any]) -> Optional[Any]:
    """
    Build a UCNSStore from markers_inventory.
    Keys: '{prefix}:{normalized_phrase}' (e.g. 'R.hard:i cannot do that').
    Single-token phrases encode to depth-1 (bytes); multi-token to depth-2 (list of bytes).
    Returns None if ucns_recursive is not installed.
    """
    if not _UCNS_AVAILABLE:
        return None

    store = UCNSStore()
    mm = markers_inventory.get("metric_marker_sets", {})

    for metric_key, list_key, prefix in _PHRASE_MAP:
        phrases = (
            (mm.get(metric_key, {}) or {}).get("tier_a_structural", {}) or {}
        ).get(list_key, []) or []

        for phrase in phrases:
            if not phrase:
                continue
            words = [normalize_text_for_matching(w) for w in phrase.split() if w]
            if not words:
                continue
            key = f"{prefix}:{' '.join(words)}"
            payload: Any = (
                words[0].encode("utf-8") if len(words) == 1
                else [w.encode("utf-8") for w in words]
            )
            store.insert(key, payload)

    return store


def ucns_hits_for_turn(store: Any, tokens: List[str]) -> Dict[str, int]:
    """
    Sliding-window UCNS query over turn tokens.

    For each n-gram (n=1.._MAX_PHRASE_TOKENS), encodes the window via
    recursive_encode and calls store.left_factors().  Exact matches
    (remainder is None, meaning stored_object == query_window) increment
    the count for that store key.

    Non-overlapping enforcement is NOT applied — Phase 1 produces raw counts
    for direct comparison with match_phrases_in_turn_tokens output.

    Returns {store_key: hit_count}.
    """
    if not _UCNS_AVAILABLE or not tokens:
        return {}

    ntoks = [normalize_text_for_matching(t) for t in tokens]
    n = len(ntoks)
    counts: Dict[str, int] = {}

    for length in range(1, min(_MAX_PHRASE_TOKENS, n) + 1):
        for start in range(n - length + 1):
            window = ntoks[start : start + length]
            payload: Any = (
                window[0].encode("utf-8") if length == 1
                else [w.encode("utf-8") for w in window]
            )
            try:
                q = recursive_encode(payload)
            except Exception:
                continue
            for key, remainder in store.left_factors(q):
                if remainder is None:
                    counts[key] = counts.get(key, 0) + 1

    return counts
# ratios: loc_comments=70:19 imports_exports=4:2 calls_definitions=19:2
