"""Polarity-balance regression test for the bones word inventory.

Frozen canon principle (bones_words_v1.json _meta.polarity_balance_principle):
    If the negative pole of a category is a bone, the affirmative pole must
    also be a bone. Otherwise the instrument carries built-in observer bias.

This test is the freeze enforcer for that principle: it fails if a
negative-pole adverb is present without its affirmative counterpart.
"""

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORDS_PATH = REPO_ROOT / "backend" / "src" / "edcmbone" / "canon" / "data" / "bones_words_v1.json"


def _word_tokens():
    data = json.loads(WORDS_PATH.read_text(encoding="utf-8"))
    return {e["word"].lower() for e in data["words"]}


# (negative_pole, affirmative_pole) pairs that must both be present.
POLARITY_PAIRS = [
    ("not", "yes"),
    ("never", "always"),
    ("nothing", "something"),
    ("nobody", "somebody"),
    ("nowhere", "somewhere"),
    ("none", "some"),
    ("neither", "either"),
    ("rarely", "often"),
    ("seldom", "frequently"),
    # Near-negation group: hardly/scarcely/barely now balanced by fully/completely.
    ("hardly", "fully"),
    ("barely", "completely"),
]


def test_polarity_balance_adverbs():
    tokens = _word_tokens()
    for neg, pos in POLARITY_PAIRS:
        assert neg in tokens, f"negative pole missing: {neg!r}"
        assert pos in tokens, f"affirmative pole missing for {neg!r}: {pos!r}"


def test_near_negation_group_has_affirmative_coverage():
    """All three near-negation adverbs are present, and so are both
    affirmative-pole completion adverbs that balance them."""
    tokens = _word_tokens()
    for neg in ("hardly", "scarcely", "barely"):
        assert neg in tokens, f"near-negation pole missing: {neg!r}"
    for pos in ("fully", "completely"):
        assert pos in tokens, f"affirmative completion pole missing: {pos!r}"
