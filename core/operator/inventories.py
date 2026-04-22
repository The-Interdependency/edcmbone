# core/operator/inventories.py
# hmmm: flexible loader; supports canon_eng bones/affixes JSON shapes.

from __future__ import annotations

from typing import Any, Dict, Tuple

FAMILIES = ("P", "K", "Q", "T", "S")


def load_bones_map(bones_inv: Dict[str, Any]) -> Dict[str, str]:
    """
    Build token→family map from bones_v1.json closed_class_mapping and
    contraction fragment_family_map.
    """
    result: Dict[str, str] = {}

    ccm = bones_inv.get("closed_class_mapping", {})
    for family, subcats in ccm.items():
        if not isinstance(subcats, dict):
            continue
        for subcat, tokens in subcats.items():
            if subcat == "notes":
                continue
            if isinstance(tokens, list):
                for tok in tokens:
                    if isinstance(tok, str):
                        result[tok.lower()] = str(family)

    # contraction fragments (n't → Q, 'll → T, etc.)
    fragment_map = bones_inv.get("contractions", {}).get("fragment_family_map", {})
    for frag, family in fragment_map.items():
        result[str(frag).lower()] = str(family)

    return result


def load_affixes(affixes_inv: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Returns (prefix_map, suffix_map) mapping affix→family.
    Accepts:
      list form: [{"affix": "un", "family": "Q"}, ...]  (canon_eng/affixes_v1.json)
      dict form: {"un": "Q", ...}
      flat keys: {"pre:un": "Q", "suf:ing": "S", ...}  (fallback)
    """
    pref: Dict[str, str] = {}
    suf: Dict[str, str] = {}

    raw_pref = affixes_inv.get("prefixes", {})
    raw_suf = affixes_inv.get("suffixes", {})

    if isinstance(raw_pref, list):
        for item in raw_pref:
            if isinstance(item, dict) and "affix" in item and "family" in item:
                pref[str(item["affix"]).lower()] = str(item["family"])
    elif isinstance(raw_pref, dict):
        pref = {k.lower(): str(v) for k, v in raw_pref.items()}

    if isinstance(raw_suf, list):
        for item in raw_suf:
            if isinstance(item, dict) and "affix" in item and "family" in item:
                suf[str(item["affix"]).lower()] = str(item["family"])
    elif isinstance(raw_suf, dict):
        suf = {k.lower(): str(v) for k, v in raw_suf.items()}

    if not pref and not suf:
        # fallback: flat keys like "pre:un" / "suf:ing"
        for k, v in affixes_inv.items():
            if not isinstance(v, str):
                continue
            ks = str(k).lower()
            if ks.startswith("pre:"):
                pref[ks[4:]] = v
            elif ks.startswith("suf:"):
                suf[ks[4:]] = v

    return pref, suf
