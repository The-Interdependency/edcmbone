# core/parsing/tokenizer.py
# hmmm: must satisfy tokenization invariants from spec appendix:
# - preserve punctuation as separate tokens
# - preserve apostrophe fragments
# - preserve hyphenated compounds as ONE surface token
# - preserve em dash as its own token

from __future__ import annotations

import re
from typing import List

# Keep em dash and en dash as their own tokens.
# Keep hyphenated compounds as one token (letters/digits joined by hyphen).
# Keep contractions as one token at surface stage (split later in operator).
TOKEN_RE = re.compile(
    r"""
    (—|–)                              # em dash or en dash
  | (\?\!+|\?+|\!+)                    # ? !! ??? etc.
  | ([A-Za-z0-9]+(?:-[A-Za-z0-9]+)+)   # hyphenated compound
  | ([A-Za-z0-9]+(?:'[A-Za-z0-9]+)*)   # word with apostrophes
  | ([/\\])                            # slash (kept as token; operator ignores v1)
  | ([\.\,\:\;\(\)\[\]\{\}"])          # common punctuation (quote as token)
  """,
    re.VERBOSE,
)

def tokens_surface(text: str) -> List[str]:
    if not text:
        return []
    toks: List[str] = []
    for m in TOKEN_RE.finditer(text):
        tok = next(g for g in m.groups() if g is not None)
        toks.append(tok)
    # If regex misses odd unicode, fall back by splitting remaining whitespace chunks
    # (rare, but keeps determinism).
    if not toks:
        toks = text.split()
    return toks
