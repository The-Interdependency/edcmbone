# core/behavioral/marker_matcher.py
# hmmm: longest-phrase-first matching, non-overlapping per text.

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple
from core.parsing.normalizer import normalize_text_for_matching

@dataclass
class Hit:
    tier: str
    marker_id: str
    weight: float
    matched_text: str
    turn_id: str
    start_token: int
    end_token: int

def _compile_phrases(phrases: List[str]) -> List[str]:
    # lower + sort by length desc
    ph = [normalize_text_for_matching(p) for p in phrases if p]
    ph.sort(key=len, reverse=True)
    return ph

def match_phrases_in_turn_tokens(
    *,
    turn_id: str,
    tokens: List[str],
    phrases: List[str],
    marker_prefix: str,
    tier: str,
    weight: float
) -> List[Hit]:
    """
    Matches phrases over token sequences (space-joined).
    Longest-first, greedy non-overlapping.
    """
    if not phrases or not tokens:
        return []
    # normalize tokens
    ntoks = [normalize_text_for_matching(t) for t in tokens]
    text = " ".join(ntoks)

    compiled = _compile_phrases(phrases)
    hits: List[Hit] = []
    used = [False] * len(ntoks)

    # phrase matching by scanning token windows
    for ph in compiled:
        ph_toks = ph.split()
        L = len(ph_toks)
        if L == 0:
            continue
        for i in range(0, len(ntoks) - L + 1):
            if any(used[i:i+L]):
                continue
            if ntoks[i:i+L] == ph_toks:
                for j in range(i, i+L):
                    used[j] = True
                hits.append(Hit(
                    tier=tier,
                    marker_id=f"{marker_prefix}:{ph}",
                    weight=weight,
                    matched_text=ph,
                    turn_id=turn_id,
                    start_token=i,
                    end_token=i+L-1
                ))
    return hits
