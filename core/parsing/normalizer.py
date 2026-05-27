# core/parsing/normalizer.py
# hmmm: normalization for matching; raw_text remains lossless elsewhere.

from __future__ import annotations

def normalize_text_for_matching(s: str) -> str:
    # Lowercase + normalize both smart-quote apostrophe variants to plain "’"
    return (
        (s or "")
        .replace("’", "'")  # right single quotation mark -> ASCII apostrophe
        .replace("‘", "'")  # left single quotation mark -> ASCII apostrophe
        .replace("‛", "'")  # single high-reversed-9 quotation mark -> ASCII apostrophe
        .lower()
    )
