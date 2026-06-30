import re
from pathlib import Path

from core.parsing.normalizer import normalize_text_for_matching


def _parser_word_re():
    repo_root = Path(__file__).resolve().parents[1]
    src_path = repo_root / "backend_old" / "src" / "edcmbone" / "parser" / "turns_rounds.py"
    src = src_path.read_text()
    m = re.search(r"_WORD_RE\s*=\s*re\.compile\(r\"([^\"]+)\"\)", src)
    assert m, "Could not locate _WORD_RE in parser/turns_rounds.py"
    return re.compile(m.group(1))


def _parser_raw_tokens_like_impl(text: str):
    word_re = _parser_word_re()
    text = (text or "").replace("’", "'").replace("‘", "'")
    return word_re.findall(text)


def test_normalize_text_for_matching_maps_smart_to_ascii_apostrophe():
    text = "don’t can‘t it’s"
    out = normalize_text_for_matching(text)
    assert out == "don't can't it's"


def test_parser_word_re_keeps_ascii_contractions_whole():
    tokens = _parser_raw_tokens_like_impl("don't can't it's")
    assert tokens == ["don't", "can't", "it's"]


def test_parser_word_re_keeps_smart_contractions_whole_after_normalization():
    normalized = normalize_text_for_matching("don’t can’t it’s")
    tokens = _parser_raw_tokens_like_impl(normalized)
    assert tokens == ["don't", "can't", "it's"]


def test_parser_word_re_keeps_hyphenated_compounds_as_one_surface_token():
    tokens = _parser_raw_tokens_like_impl("state-of-the-art")
    assert tokens == ["state-of-the-art"]
