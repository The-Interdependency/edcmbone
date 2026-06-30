# ratios: loc_comments=115:43 imports_exports=2:1 calls_definitions=25:3
# === MODULE_BUILD ===
# id: operator_tokenization
#   module_name: operator tokenizer
#   module_kind: engine
#   summary: tokenizes turns and maps closed-class tokens into operator families with canon-priority rules.
#   owner: edcmbone-maintainers
#   public_surface: tokenize_turn
#   internal_surface: _family,_normalize_apos,_WORD_FAMILY,_FRAG_FAMILY,_STANDALONE_PUNCT
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_apostrophe_normalization_and_tokenization.py,tests/test_backend.py
#   rollout: default_enabled
#   rollback: swap callers to legacy tokenizer and remove export
# === END MODULE_BUILD ===
"""
Operator-layer tokenizer.
Maps surface tokens to bone families per bones_v1.json (frozen v1.0.0).
Collision priority: P > K > Q > T > S.
Zero external dependencies; stdlib only.
"""
from __future__ import annotations
from typing import Optional

# ── Closed-class inventories (source: canon_eng/bones_v1.json, frozen) ────────

_S_RAW: frozenset[str] = frozenset({
    "a", "an", "the",
    "this", "that", "these", "those",
    "my", "your", "his", "her", "its", "our", "their",
    "mine", "yours", "hers", "ours", "theirs",
    "each", "every", "either", "neither", "some", "any", "no",
    "another", "other", "others", "such", "same",
    "i", "me", "you", "he", "him", "she", "her", "it", "we", "us", "they", "them",
    "myself", "yourself", "yourselves", "himself", "herself",
    "itself", "ourselves", "themselves",
    "someone", "somebody", "something",
    "anyone", "anybody", "anything",
    "everyone", "everybody", "everything",
    "noone", "nobody", "nothing",
    "who", "whom", "whose", "which", "that",
    "there", "here", "now", "then",
})

_T_RAW: frozenset[str] = frozenset({
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had",
    "do", "does", "did",
    "can", "could", "may", "might", "must", "shall", "should", "will", "would",
    "now", "then", "today", "tomorrow", "yesterday",
    "already", "still", "yet",
})

_Q_RAW: frozenset[str] = frozenset({
    "not", "no", "never", "none", "nothing", "nobody", "neither", "nor",
    "all", "some", "any", "many", "much", "few", "several",
    "most", "more", "less", "least", "enough",
    "very", "too", "only", "just", "also", "even", "quite", "rather", "almost",
    "who", "what", "when", "where", "why", "how", "which", "whom", "whose",
    "yes", "yeah", "yep", "nope", "nah", "okay", "ok",
})

_K_RAW: frozenset[str] = frozenset({
    "and", "but", "or", "nor", "yet", "so",
    "because", "although", "though", "since", "while", "whereas",
    "if", "unless", "until", "when", "whenever", "where", "wherever",
    "before", "after", "once", "than", "that",
    "either", "neither", "both", "whether",
    "however", "therefore", "thus", "moreover", "instead", "otherwise",
})

_P_RAW: frozenset[str] = frozenset({
    "in", "on", "at", "by", "with", "without", "for", "from", "to", "of", "off",
    "into", "onto", "out", "over", "under", "above", "below", "before", "after",
    "between", "among", "within", "beyond", "through", "across", "against", "around",
    "near", "along", "amid", "during", "via", "per", "upon", "beneath", "behind",
    "beside", "besides", "inside", "outside", "toward", "towards", "past",
    "than", "as",
    "because", "despite", "except", "like", "unlike",
})

# Build collision-resolved lookup.
# Process lowest priority first (S); higher priority overwrites.
_WORD_FAMILY: dict[str, str] = {}
for _w in _S_RAW: _WORD_FAMILY[_w] = "S"
for _w in _T_RAW: _WORD_FAMILY[_w] = "T"
for _w in _Q_RAW: _WORD_FAMILY[_w] = "Q"
for _w in _K_RAW: _WORD_FAMILY[_w] = "K"
for _w in _P_RAW: _WORD_FAMILY[_w] = "P"

# Contraction fragment family map (normalized: standard apostrophe)
_FRAG_FAMILY: dict[str, str] = {
    "n't": "Q", "'t": "Q",
    "'ll": "T", "'d": "T", "'re": "T", "'m": "T", "'ve": "T", "'s": "T",
}

# Standalone punctuation → emitted (surface, family) tuples
_STANDALONE_PUNCT: dict[str, list[tuple[str, str]]] = {
    "?": [("?", "Q")],
    "–": [("–", "K")],   # en dash
    ";": [(";", "K")],
    ":": [(":", "K")],
    "—": [],                   # em dash: preserved, emits no operator
    "/": [],                        # ignored in v1
}


def _family(word: str) -> Optional[str]:
    return _WORD_FAMILY.get(word.lower())


def _normalize_apos(s: str) -> str:
    return s.replace("’", "'").replace("‘", "'")


def tokenize_turn(text: str) -> list[tuple[str, Optional[str]]]:
    """
    Split a turn into (surface, family) pairs.

    family is None for open-class (flesh) tokens.
    Bone family labels: P | K | Q | T | S.

    Rules applied (per bones_v1.json):
    - Collision priority P > K > Q > T > S resolves multi-family words.
    - Hyphenated compounds: emit 1 K for the compound, then classify each part.
    - Contractions: split on apostrophe; map fragment via _FRAG_FAMILY.
    - Standalone punctuation: ?, en-dash, ;, : emit K or Q; em-dash and / emit nothing.
    - Trailing . ! , are stripped; trailing ? emits a Q token.
    """
    out: list[tuple[str, Optional[str]]] = []

    for raw in text.split():
        tok = _normalize_apos(raw)

        if tok in _STANDALONE_PUNCT:
            out.extend(_STANDALONE_PUNCT[tok])
            continue

        # Strip trailing . ! , ? — collect any trailing ?
        stem = tok
        trailing_q = 0
        while stem and stem[-1] in ".!,?":
            if stem[-1] == "?":
                trailing_q += 1
            stem = stem[:-1]

        if not stem:
            out.extend([("?", "Q")] * trailing_q)
            continue

        # Hyphenated compound: emit 1 K, then classify each part
        if "-" in stem and not stem.startswith("-") and not stem.endswith("-"):
            parts = [p for p in stem.split("-") if p]
            out.append((stem, "K"))
            for part in parts:
                fam = _family(part)
                if fam is not None:
                    out.append((part, fam))

        # n't contraction (must precede generic apostrophe check)
        elif stem.lower().endswith("n't"):
            base = stem[:-3]
            if base:
                out.append((base, _family(base)))
            out.append(("n't", "Q"))

        # Generic apostrophe contraction
        elif "'" in stem:
            idx = stem.index("'")
            base = stem[:idx]
            frag = stem[idx:]   # includes apostrophe
            fam_frag = _FRAG_FAMILY.get(frag.lower())
            if base:
                out.append((base, _family(base)))
            if frag:
                out.append((frag, fam_frag))

        else:
            out.append((stem, _family(stem)))

        out.extend([("?", "Q")] * trailing_q)

    return out
# ratios: loc_comments=115:43 imports_exports=2:1 calls_definitions=25:3
