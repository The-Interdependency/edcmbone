# core/operator/matcher.py
# hmmm: whole-word precedence; affix stripping only if no whole-word bone match.

from __future__ import annotations

from typing import Dict, List, Tuple
from core.parsing.normalizer import normalize_text_for_matching

COLLISION_PRIORITY = ["P", "K", "Q", "T", "S"]

def choose_family(families: List[str]) -> str:
    famset = set(families)
    for f in COLLISION_PRIORITY:
        if f in famset:
            return f
    return families[0] if families else "S"

def contraction_split(tok: str) -> List[str]:
    """
    Surface contraction splitting aligned to fragment_family_map in bones_v1.json:
      don't -> do + n't
      I'll  -> I + 'll
      I'd   -> I + 'd
      we're -> we + 're
      I'm   -> I + 'm
      I've  -> I + 've
      it's  -> it + 's
    """
    t = tok
    if not t or "'" not in t:
        return [tok]
    low = t.lower()
    if low.endswith("n't") and len(t) > 3:
        return [t[:-3], "n't"]
    for suf in ("'ll", "'d", "'re", "'m", "'ve", "'s"):
        if low.endswith(suf) and len(t) > len(suf):
            return [t[:-len(suf)], suf]
    return [tok]

def match_whole_word(tok: str, bones_map: Dict[str, str]) -> List[str]:
    t = normalize_text_for_matching(tok)
    fam = bones_map.get(t)
    return [fam] if fam in {"P","K","Q","T","S"} else []

def match_punct(tok: str) -> List[str]:
    # frozen punct rules per bones_v1.json punctuation_rules
    if tok == "?":
        return ["Q"]
    if tok == "—":
        return []  # em dash emits zero
    if tok == "–":
        return ["K"]  # en dash as connector
    if tok in (":", ";"):
        return ["K"]  # connective emissions per canon
    # hyphen handled separately at surface token stage
    return []

def hyphen_compound_emission(tok: str) -> List[str]:
    # If token contains hyphen and is alnum-hyphen compound, emit exactly one K.
    if "-" in tok:
        return ["K"]
    return []

def match_affixes(tok: str, prefix_map: Dict[str, str], suffix_map: Dict[str, str], valid_stems: set[str] | None = None) -> Tuple[List[str], str]:
    """
    Longest-match-first; prefix then suffix; emit ALL matched affixes.
    Returns (families_emitted, residual_root).
    
    When valid_stems is provided, validation is deferred until after all affixes
    are stripped. This allows multi-affix words like "redoing" (re+do+ing) to work
    correctly even when intermediate forms like "doing" are not in valid_stems.
    """
    t = normalize_text_for_matching(tok)
    fams: List[str] = []
    root = t

    # sort once (longest first) before the repeated-match loops
    pref_list = sorted(prefix_map.keys(), key=len, reverse=True)
    changed = True
    while changed:
        changed = False
        for p in pref_list:
            if root.startswith(p) and len(root) > len(p):
                residual = root[len(p):]
                fams.append(prefix_map[p])
                root = residual
                changed = True
                break

    suf_list = sorted(suffix_map.keys(), key=len, reverse=True)
    changed = True
    while changed:
        changed = False
        for s in suf_list:
            if root.endswith(s) and len(root) > len(s):
                residual = root[:-len(s)]
                fams.append(suffix_map[s])
                root = residual
                changed = True
                break

    # Validate final root against valid_stems if provided.
    # If validation fails, return no affixes (treat as unmatched).
    if valid_stems is not None and fams and root not in valid_stems:
        return [], t

    return fams, root
