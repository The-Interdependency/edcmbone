"""
Tests for the edcmbone backend library.

Covers:
  - edcmbone.canon    (CanonLoader)
  - edcmbone.parser   (parse_transcript, Turn, Round, BoneToken, FleshToken)
  - edcmbone.metrics  (stats, risk, compute)
  - edcmbone.compress (encode/decode round-trip, compression_stats)
"""

import math
import pytest

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

TRANSCRIPT_2SPK = """\
A: Can you help me understand why this isn't working?
B: I can't diagnose the issue without more context. However, if you share the error I won't refuse to help.
A: That's not very helpful. Don't you think you should at least try?
B: You're right. What specifically breaks when you run it?
"""

TRANSCRIPT_MULTIFORMAT = """\
**User**: Is this working or not?
**Assistant**: I cannot confirm without more information.
"""

TRANSCRIPT_BRACKET = """\
[Alice]: Never do that again.
[Bob]: I disagree completely.
"""


@pytest.fixture(scope="module")
def canon():
    from edcmbone.canon import CanonLoader
    return CanonLoader()


@pytest.fixture(scope="module")
def parsed(canon):
    from edcmbone.parser import parse_transcript
    return parse_transcript(TRANSCRIPT_2SPK, canon=canon)


@pytest.fixture(scope="module")
def metrics(parsed, canon):
    from edcmbone.metrics import compute_transcript
    return compute_transcript(parsed, canon=canon)


# ---------------------------------------------------------------------------
# canon
# ---------------------------------------------------------------------------

class TestCanonLoader:
    def test_lookup_word_known(self, canon):
        result = canon.lookup_word("not")
        assert result is not None
        assert result["primary"] == "P"
        assert "P" in result["families"]

    def test_lookup_word_unknown(self, canon):
        assert canon.lookup_word("xyzzy_unknown_word") is None

    def test_lookup_word_case_insensitive(self, canon):
        lower = canon.lookup_word("not")
        upper = canon.lookup_word("NOT")
        assert lower == upper

    def test_lookup_multiword(self, canon):
        result = canon.lookup_word("of course")
        assert result is not None
        assert result.get("joined") is not None

    def test_lookup_affix_prefix(self, canon):
        result = canon.lookup_affix("un-")
        assert result is not None
        assert result["primary"] == "P"

    def test_lookup_affix_suffix(self, canon):
        result = canon.lookup_affix("-ness")
        assert result is not None

    def test_lookup_affix_unknown(self, canon):
        assert canon.lookup_affix("zzz-") is None

    def test_lookup_punct_question(self, canon):
        result = canon.lookup_punct("?")
        assert result is not None
        assert result["primary"] == "Q"
        assert result["tokens_emitted"] == 1

    def test_lookup_punct_period_boundary(self, canon):
        result = canon.lookup_punct(".")
        assert result is not None
        assert result["tokens_emitted"] == 0

    def test_metric_names(self, canon):
        names = canon.metric_names()
        assert set(names) == {"C", "R", "D", "N", "L", "O", "F", "E", "I"}
        assert len(names) == 9

    def test_metric_info_keys(self, canon):
        info = canon.metric_info("R")
        assert "formula" in info
        assert "markers" in info
        assert "computable_from_markers" in info

    def test_metric_info_unknown_raises(self, canon):
        with pytest.raises(KeyError):
            canon.metric_info("Z")

    def test_marker_phrases(self, canon):
        info = canon.metric_info("R")
        first_cat = list(info["markers"].keys())[0]
        phrases = canon.marker_phrases("R", first_cat)
        assert isinstance(phrases, list)
        assert len(phrases) > 0

    def test_all_words_count(self, canon):
        words = canon.all_words()
        assert len(words) == 253

    def test_all_affixes_count(self, canon):
        affixes = canon.all_affixes()
        assert len(affixes) == 76

    def test_all_punct_count(self, canon):
        punct = canon.all_punct()
        assert len(punct) == 13

    def test_meta_version(self, canon):
        meta = canon.meta("words")
        assert meta.get("version") == "1.0.0"

    def test_meta_unknown_raises(self, canon):
        with pytest.raises(KeyError):
            canon.meta("nonexistent")


# ---------------------------------------------------------------------------
# parser
# ---------------------------------------------------------------------------

class TestParser:
    def test_returns_parsed_transcript(self, parsed):
        from edcmbone.parser import ParsedTranscript
        assert isinstance(parsed, ParsedTranscript)

    def test_speaker_detection(self, parsed):
        assert "A" in parsed.speakers
        assert "B" in parsed.speakers

    def test_round_count(self, parsed):
        # 4 turns (A B A B) with cycle strategy = 2 rounds
        assert len(parsed.rounds) == 2

    def test_turn_count(self, parsed):
        assert len(parsed.turns) == 4

    def test_bone_tokens_present(self, parsed):
        from edcmbone.parser import BoneToken
        all_bones = [t for turn in parsed.turns for t in turn.tokens
                     if isinstance(t, BoneToken)]
        assert len(all_bones) > 0

    def test_boundary_punct_is_flesh(self, parsed):
        from edcmbone.parser import BoneToken
        # Period and comma have tokens_emitted=0, must NOT be BoneToken
        boundary_marks = {".", ","}
        for turn in parsed.turns:
            for tok in turn.tokens:
                if isinstance(tok, BoneToken) and tok.surface in boundary_marks:
                    pytest.fail(f"Boundary mark {tok.surface!r} classified as bone")

    def test_active_punct_is_bone(self, parsed):
        from edcmbone.parser import BoneToken
        # "?" should appear as a bone with primary Q
        q_bones = [t for turn in parsed.turns for t in turn.tokens
                   if isinstance(t, BoneToken) and t.surface == "?" and t.primary == "Q"]
        assert len(q_bones) > 0

    def test_family_counts_keys(self, parsed):
        for turn in parsed.turns:
            for k in turn.family_counts:
                assert k in ("P", "K", "Q", "T", "S")

    def test_round_bone_count_consistent(self, parsed):
        for rnd in parsed.rounds:
            expected = sum(t.bone_count for t in rnd.turns)
            assert rnd.bone_count == expected

    def test_markdown_bold_format(self, canon):
        from edcmbone.parser import parse_transcript
        pt = parse_transcript(TRANSCRIPT_MULTIFORMAT, canon=canon)
        assert "User" in pt.speakers
        assert "Assistant" in pt.speakers

    def test_bracket_format(self, canon):
        from edcmbone.parser import parse_transcript
        pt = parse_transcript(TRANSCRIPT_BRACKET, canon=canon)
        assert "Alice" in pt.speakers
        assert "Bob" in pt.speakers

    def test_pairs_strategy(self, canon):
        from edcmbone.parser import parse_transcript
        pt = parse_transcript(TRANSCRIPT_2SPK, round_strategy="pairs", canon=canon)
        assert len(pt.rounds) == 2
        for rnd in pt.rounds:
            assert len(rnd.turns) <= 2

    def test_affix_stripping(self, canon):
        from edcmbone.parser import parse_transcript, BoneToken
        # "unhappy" should be caught by un- prefix stripping
        pt = parse_transcript("A: That is completely unhappy.\nB: Yes.", canon=canon)
        all_bones = [t for turn in pt.turns for t in turn.tokens
                     if isinstance(t, BoneToken)]
        affix_bones = [b for b in all_bones if b.bone_type == "affix"]
        assert len(affix_bones) > 0


# ---------------------------------------------------------------------------
# metrics.stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_tokenize_basic(self):
        from edcmbone.metrics import tokenize
        tokens = tokenize("Hello, world!")
        assert "hello" in tokens
        assert "world" in tokens

    def test_ttr_all_unique(self):
        from edcmbone.metrics import ttr
        assert ttr(["a", "b", "c"]) == pytest.approx(1.0)

    def test_ttr_all_same(self):
        from edcmbone.metrics import ttr
        assert ttr(["a", "a", "a"]) == pytest.approx(1 / 3)

    def test_ttr_empty(self):
        from edcmbone.metrics import ttr
        assert ttr([]) == 0.0

    def test_repetition_ratio(self):
        from edcmbone.metrics import repetition_ratio, ttr
        tokens = ["a", "b", "a"]
        assert repetition_ratio(tokens) == pytest.approx(1.0 - ttr(tokens))

    def test_shannon_entropy_uniform(self):
        from edcmbone.metrics import shannon_entropy
        # 4 equally-likely symbols -> entropy = 2 bits
        tokens = ["a", "b", "c", "d"] * 10
        assert shannon_entropy(tokens) == pytest.approx(2.0, abs=0.01)

    def test_shannon_entropy_empty(self):
        from edcmbone.metrics import shannon_entropy
        assert shannon_entropy([]) == 0.0

    def test_novelty_all_new(self):
        from edcmbone.metrics import novelty
        assert novelty(["x", "y"], ["a", "b"]) == pytest.approx(1.0)

    def test_novelty_all_old(self):
        from edcmbone.metrics import novelty
        assert novelty(["a", "b"], ["a", "b"]) == pytest.approx(0.0)

    def test_cosine_identical(self):
        from edcmbone.metrics import cosine_sim
        tokens = ["a", "b", "c"]
        assert cosine_sim(tokens, tokens) == pytest.approx(1.0)

    def test_cosine_orthogonal(self):
        from edcmbone.metrics import cosine_sim
        assert cosine_sim(["a", "b"], ["c", "d"]) == pytest.approx(0.0)

    def test_cosine_empty(self):
        from edcmbone.metrics import cosine_sim
        assert cosine_sim([], ["a"]) == 0.0

    def test_jaccard_identical(self):
        from edcmbone.metrics import jaccard
        assert jaccard({"a", "b"}, {"a", "b"}) == pytest.approx(1.0)

    def test_jaccard_disjoint(self):
        from edcmbone.metrics import jaccard
        assert jaccard({"a"}, {"b"}) == pytest.approx(0.0)

    def test_clamp(self):
        from edcmbone.metrics import clamp
        assert clamp(-1.0) == 0.0
        assert clamp(2.0) == 1.0
        assert clamp(0.5) == pytest.approx(0.5)

    def test_rep_ngram_density_no_repeats(self):
        from edcmbone.metrics import rep_ngram_density
        tokens = ["a", "b", "c", "d", "e"]
        assert rep_ngram_density(tokens, n=3) == pytest.approx(0.0)

    def test_rep_ngram_density_with_repeats(self):
        from edcmbone.metrics import rep_ngram_density
        # "a b c" repeated twice
        tokens = ["a", "b", "c", "a", "b", "c"]
        assert rep_ngram_density(tokens, n=3) > 0.0


# ---------------------------------------------------------------------------
# metrics.risk
# ---------------------------------------------------------------------------

class TestRisk:
    def test_fixation_risk_clamped(self):
        from edcmbone.metrics import fixation_risk
        result = fixation_risk(["a"] * 20, ["b"] * 20)
        assert 0.0 <= result <= 1.0

    def test_fixation_risk_high_repetition(self):
        from edcmbone.metrics import fixation_risk
        repetitive = ["the"] * 50
        varied_prev = list("abcdefghijklmnopqrstuvwxyz")
        high = fixation_risk(repetitive, varied_prev)
        assert high > 0.3

    def test_loop_risk_clamped(self):
        from edcmbone.metrics import loop_risk
        result = loop_risk(["a", "b"], ["a", "b", "c"])
        assert 0.0 <= result <= 1.0

    def test_escalation_risk_clamped(self):
        from edcmbone.metrics import escalation_risk
        result = escalation_risk(["a"], ["b"], ["c"], 0.0, 0.0)
        assert 0.0 <= result <= 1.0

    def test_stagnation_risk_clamped(self):
        from edcmbone.metrics import stagnation_risk
        result = stagnation_risk(0.0, ["a"], ["a"], 0.5)
        assert 0.0 <= result <= 1.0


# ---------------------------------------------------------------------------
# metrics.compute
# ---------------------------------------------------------------------------

class TestCompute:
    def test_returns_list(self, metrics):
        assert isinstance(metrics, list)

    def test_one_metric_per_round(self, parsed, metrics):
        assert len(metrics) == len(parsed.rounds)

    def test_all_metrics_in_range(self, metrics):
        for m in metrics:
            for attr in ("C", "R", "F", "E", "D", "N", "I", "L", "P"):
                val = getattr(m, attr)
                assert 0.0 <= val <= 1.0, f"{attr}={val} out of [0,1]"
            assert -1.0 <= m.O <= 1.0, f"O={m.O} out of [-1,1]"
            assert m.kappa >= 0.0

    def test_vector_length(self, metrics):
        for m in metrics:
            assert len(m.vector()) == 11

    def test_as_dict_keys(self, metrics):
        d = metrics[0].as_dict()
        for key in ("C", "R", "F", "E", "D", "N", "I", "O", "L", "P", "kappa"):
            assert key in d

    def test_kappa_increases_with_dissonance(self, parsed, canon):
        from edcmbone.metrics.compute import compute_round, energy_step
        # Artificially high dissonance -> kappa should grow
        _, kappa = energy_step(0.0, 0.0, dissonance=0.9, alpha=0.9, delta_max=0.1)
        assert kappa > 0.0


# ---------------------------------------------------------------------------
# compress
# ---------------------------------------------------------------------------

class TestCompress:
    def test_round_trip_dict(self, parsed, metrics):
        import edcmbone.compress as codec
        encoded = codec.encode(parsed, metrics)
        pt2, m2 = codec.decode(encoded)

        assert len(pt2.turns) == len(parsed.turns)
        assert len(pt2.rounds) == len(parsed.rounds)
        for t1, t2 in zip(parsed.turns, pt2.turns):
            assert t1.speaker == t2.speaker
            assert t1.text == t2.text
            assert t1.bone_count == t2.bone_count

    def test_round_trip_bytes(self, parsed, metrics):
        import edcmbone.compress as codec
        compressed = codec.to_bytes(parsed, metrics)
        pt2, m2 = codec.from_bytes(compressed)

        assert len(pt2.turns) == len(parsed.turns)
        for m1, m2i in zip(metrics, m2):
            assert abs(m1.C - m2i.C) < 1e-9
            assert abs(m1.R - m2i.R) < 1e-9
            assert abs(m1.kappa - m2i.kappa) < 1e-9

    def test_bytes_is_bytes(self, parsed):
        import edcmbone.compress as codec
        result = codec.to_bytes(parsed)
        assert isinstance(result, bytes)

    def test_encode_without_metrics(self, parsed):
        import edcmbone.compress as codec
        encoded = codec.encode(parsed)
        pt2, m2 = codec.decode(encoded)
        assert m2 is None
        assert len(pt2.turns) == len(parsed.turns)

    def test_compression_stats_keys(self, parsed):
        import edcmbone.compress as codec
        compressed = codec.to_bytes(parsed)
        stats = codec.compression_stats(TRANSCRIPT_2SPK, compressed, parsed)
        for key in (
            "original_chars", "original_bytes", "compressed_bytes",
            "byte_compression_ratio", "structural_density",
            "bone_count", "flesh_count", "family_counts",
            "bone_entropy_bits", "huffman_min_bits", "huffman_codes",
            "bone_stream_savings_pct",
        ):
            assert key in stats, f"missing key: {key}"

    def test_structural_density_in_range(self, parsed):
        import edcmbone.compress as codec
        compressed = codec.to_bytes(parsed)
        stats = codec.compression_stats(TRANSCRIPT_2SPK, compressed, parsed)
        assert 0.0 <= stats["structural_density"] <= 1.0

    def test_huffman_codes_cover_families(self, parsed):
        import edcmbone.compress as codec
        compressed = codec.to_bytes(parsed)
        stats = codec.compression_stats(TRANSCRIPT_2SPK, compressed, parsed)
        observed_families = set(stats["family_counts"].keys())
        coded_families = set(stats["huffman_codes"].keys())
        assert observed_families == coded_families

    def test_bone_entropy_positive(self, parsed):
        import edcmbone.compress as codec
        compressed = codec.to_bytes(parsed)
        stats = codec.compression_stats(TRANSCRIPT_2SPK, compressed, parsed)
        assert stats["bone_entropy_bits"] > 0.0

    def test_format_version_in_encoded(self, parsed):
        import edcmbone.compress as codec
        encoded = codec.encode(parsed)
        assert encoded["v"] == 1
