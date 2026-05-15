from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from edcmbone.canon import CanonLoader
from edcmbone.parser.turns_rounds import _BoneClassifier, FleshToken
from core.operator.matcher import match_affixes


def test_backend_parser_affix_does_not_fire_on_invalid_residuals():
    canon = CanonLoader()
    c = _BoneClassifier(canon)
    toks = ["uncle", "unit", "universe", "under", "unique"]
    out = c.classify_sequence(toks)
    assert all((not hasattr(x, "bone_type") or x.bone_type != "affix") for x in out)


def test_backend_parser_affix_positive_cases_still_emit():
    canon = CanonLoader()
    c = _BoneClassifier(canon)
    out = c.classify_sequence(["redo"])
    assert [getattr(x, "bone_type", None) for x in out] == ["affix"]


def test_core_matcher_affix_respects_valid_stems_negative_and_positive():
    prefix_map = {"un": "P", "re": "K"}
    suffix_map = {"ing": "K"}
    valid_stems = {"happy", "do", "link"}

    fams, root = match_affixes("unhappy", prefix_map, suffix_map, valid_stems=valid_stems)
    assert fams == ["P"] and root == "happy"

    fams2, root2 = match_affixes("uncle", prefix_map, suffix_map, valid_stems=valid_stems)
    assert fams2 == [] and root2 == "uncle"
