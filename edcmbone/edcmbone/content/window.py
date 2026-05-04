"""
Content-layer window aggregation.
Aggregates ContentVectors from multiple claims over a turn/round window.
"""
from __future__ import annotations
from typing import NamedTuple, Sequence
from .vector import ContentVector, null_vector, average_ratings
from .status import TruthStatus, VerificationStatus, FoundationStatus, SpeechAct
from .rating import ContentRatings


class ContentWindow(NamedTuple):
    """Aggregated content-layer reading over a window of claims."""
    claim_count: int
    mean_ratings: ContentRatings
    truth_distribution: dict        # TruthStatus.value → fraction
    verification_distribution: dict
    foundation_distribution: dict
    speech_act_distribution: dict


def aggregate_window(vectors: Sequence[ContentVector]) -> ContentWindow:
    """Aggregate a sequence of ContentVectors into a window summary."""
    vs = list(vectors)
    n = len(vs)

    def _dist(enum_cls, attr: str) -> dict:
        counts = {s.value: 0 for s in enum_cls}
        for v in vs:
            counts[getattr(v.status, attr).value] += 1
        return {k: c / n for k, c in counts.items()} if n else {s.value: 0.0 for s in enum_cls}

    return ContentWindow(
        claim_count=n,
        mean_ratings=average_ratings(vs),
        truth_distribution=_dist(TruthStatus, "truth_status"),
        verification_distribution=_dist(VerificationStatus, "verification_status"),
        foundation_distribution=_dist(FoundationStatus, "foundation_status"),
        speech_act_distribution=_dist(SpeechAct, "speech_act"),
    )
