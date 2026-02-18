# core/operator/inventories.py
# hmmm: flexible loader; supports either {"map":{...}} or flat dict.

from __future__ import annotations

from typing import Any, Dict, Tuple

FAMILIES = ("P", "K", "Q", "T", "S")

def _as_map(inv: Dict[str, Any]) -> Dict[str, str]:
    if "map" in inv and isinstance(inv["map"], dict):
        return {str(k): str(v) for k, v in inv["map"].items()}
    # allow direct mapping
    return {str(k): str(v) for k, v in inv.items() if isinstance(v, str)}

def load_bones_map(bones_inv: Dict[str, Any]) -> Dict[str, str]:
    m = _as_map(bones_inv)
    return {k.lower(): v for k, v in m.items()}

def load_affixes(affixes_inv: Dict[str, Any]) -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Returns (prefix_map, suffix_map) mapping affix->family.
    Accepts:
      {"prefixes": {...}, "suffixes": {...}}
    or flat dict with keys like "pre:un" / "suf:ing" (fallback).
    """
    pref: Dict[str, str] = {}
    suf: Dict[str, str] = {}

    if "prefixes" in affixes_inv and isinstance(affixes_inv["prefixes"], dict):
        pref = {k.lower(): str(v) for k, v in affixes_inv["prefixes"].items()}
    if "suffixes" in affixes_inv and isinstance(affixes_inv["suffixes"], dict):
        suf = {k.lower(): str(v) for k, v in affixes_inv["suffixes"].items()}

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
