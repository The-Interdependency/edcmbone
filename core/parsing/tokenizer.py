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
    pos = 0
    for m in TOKEN_RE.finditer(text):
        # Emit any unmatched non-whitespace characters in the gap before this match.
        gap = text[pos:m.start()]
        toks.extend(gap.split())
        tok = next(g for g in m.groups() if g is not None)
        toks.append(tok)
        pos = m.end()
    # Trailing gap after the last match.
    toks.extend(text[pos:].split())
    if not toks:
        toks = text.split()
    return toks
