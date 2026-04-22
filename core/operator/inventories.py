# core/operator/inventories.py
# hmmm: flexible loader; supports either {"map":{...}} or flat dict.

from __future__ import annotations

from typing import Any, Dict, List, Tuple

FAMILIES = ("P", "K", "Q", "T", "S")

def _as_map(inv: Dict[str, Any]) -> Dict[str, str]:
    if "map" in inv and isinstance(inv["map"], dict):
        return {str(k): str(v) for k, v in inv["map"].items()}
    # allow direct mapping
    return {str(k): str(v) for k, v in inv.items() if isinstance(v, str)}

def load_bones_map(bones_inv: Dict[str, Any]) -> Dict[str, str]:
    """
    Build a token->family map from bones inventory.
    Prefers closed_class_mapping (family -> subcategory -> [tokens]) structure,
    with fallback to {"map": {...}} or flat string-valued dict.
    """
    ccm = bones_inv.get("closed_class_mapping")
    if isinstance(ccm, dict):
        result: Dict[str, str] = {}
        for family, subcats in ccm.items():
            if not isinstance(subcats, dict):
                continue
            for subcat_key, tokens in subcats.items():
                if subcat_key == "notes":
                    continue
                if isinstance(tokens, list):
                    for tok in tokens:
                        if isinstance(tok, str):
                            result[tok.lower()] = str(family)
        return result
    m = _as_map(bones_inv)
    return {k.lower(): v for k, v in m.items()}

def load_affixes(affixes_inv: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Returns (prefix_map, suffix_map) mapping affix->family.
    Accepts:
      {"prefixes": [{affix, family}, ...], "suffixes": [{affix, family}, ...]}  (list-of-objects)
      {"prefixes": {...}, "suffixes": {...}}                                      (dict)
    or flat dict with keys like "pre:un" / "suf:ing" (fallback).
    """
    pref: Dict[str, str] = {}
    suf: Dict[str, str] = {}

    raw_pref = affixes_inv.get("prefixes")
    raw_suf = affixes_inv.get("suffixes")

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
        # fallback: flat keys
        for k, v in affixes_inv.items():
            if not isinstance(v, str):
                continue
            ks = str(k).lower()
            if ks.startswith("pre:"):
                pref[ks[4:]] = v
            elif ks.startswith("suf:"):
                suf[ks[4:]] = v

    return pref, suf
