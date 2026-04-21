# core/parsing/normalizer.py
# hmmm: normalization for matching; raw_text remains lossless elsewhere.

from __future__ import annotations

def normalize_text_for_matching(s: str) -> str:
    # Lowercase + canonical apostrophe to plain "'"
    return (s or "").replace("’", "'").lower()
