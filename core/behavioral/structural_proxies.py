# core/behavioral/structural_proxies.py
# hmmm: behavioral v1 uses structural proxies as frozen in formulas.

from __future__ import annotations

from typing import Any, Dict, List
from core.parsing.normalizer import normalize_text_for_matching

def split_statements(turn: Dict[str, Any]) -> List[str]:
    # If sentence bounds not provided, treat the whole turn as one statement.
    raw = turn.get("raw_text") or ""
    return [raw] if raw else [""]

def count_question_marks(turns: List[Dict[str, Any]], turn_ids: List[str]) -> int:
    s = 0
    lookup = {t["turn_id"]: t for t in turns}
    for tid in turn_ids:
        t = lookup.get(tid)
        if not t:
            continue
        s += sum(1 for tok in t.get("tokens_surface", []) if tok == "?")
    return s

def constraint_statement_proxy_count(
    turns: List[Dict[str, Any]],
    turn_ids: List[str],
    constraint_modals: List[str],
    conditionals: List[str],
    delimiters: List[str],
) -> int:
    lookup = {t["turn_id"]: t for t in turns}
    mod = set(normalize_text_for_matching(x) for x in constraint_modals)
    con = set(normalize_text_for_matching(x) for x in conditionals)
    delim = set(normalize_text_for_matching(x) for x in delimiters)

    cs = 0
    for tid in turn_ids:
        t = lookup.get(tid)
        if not t:
            continue
        # statement = turn (v1)
        toks = [normalize_text_for_matching(x) for x in t.get("tokens_surface", [])]
        if any(x in mod for x in toks) or any(x in con for x in toks) or any(x in delim for x in toks):
            cs += 1
    return max(cs, 1)

def total_tokens_in_turn_ids(turns: List[Dict[str, Any]], turn_ids: List[str]) -> int:
    lookup = {t["turn_id"]: t for t in turns}
    tok = 0
    for tid in turn_ids:
        t = lookup.get(tid)
        if t:
            tok += len(t.get("tokens_surface", []))
    return max(tok, 1)

def detect_list_growth_pattern(user_turn: Dict[str, Any], assistant_turn: Dict[str, Any]) -> int:
    # deterministic approximation: assistant has enumerated list >= 6 items and user has no list request token.
    a = assistant_turn.get("raw_text", "").splitlines()
    count = sum(1 for line in a if line.strip().startswith(("1)", "2)", "3)", "4)", "5)", "6)", "-", "*")))
    return 1 if count >= 6 else 0
