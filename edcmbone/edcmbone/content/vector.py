"""
10D content vector: StatusFlags (4 categorical) + ContentRatings (6 scalar).
UCNS recursion depth: 3 (content = depth-3 in the layer–depth unification).
No conservation constraint — ratings are independent, status flags categorical.
"""
from __future__ import annotations
from typing import NamedTuple
from .status import (
    StatusFlags, TruthStatus, VerificationStatus,
    FoundationStatus, SpeechAct,
)
from .rating import ContentRatings

UCNS_DEPTH = 3


class ContentVector(NamedTuple):
    """
    10D content vector for a single claim.
    Embedded at UCNS depth-3 (content = depth-3 per layer–depth unification).
    """
    status: StatusFlags
    ratings: ContentRatings


def null_vector() -> ContentVector:
    """Baseline ContentVector for an unanalyzed claim."""
    return ContentVector(
        status=StatusFlags(
            truth_status=TruthStatus.UNKNOWN,
            verification_status=VerificationStatus.UNVERIFIED,
            foundation_status=FoundationStatus.ASSERTED_WITHOUT_FOUNDATION,
            speech_act=SpeechAct.UTTERED,
        ),
        ratings=ContentRatings(
            utility=0.0, clarity=0.0, focus=0.0,
            aesthetic=0.0, psychological=0.0, epistemic=0.0,
        ),
    )


def average_ratings(vectors: list[ContentVector]) -> ContentRatings:
    """Mean of scalar ratings over a list of ContentVectors."""
    if not vectors:
        return ContentRatings(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    n = len(vectors)
    return ContentRatings(
        utility=sum(v.ratings.utility for v in vectors) / n,
        clarity=sum(v.ratings.clarity for v in vectors) / n,
        focus=sum(v.ratings.focus for v in vectors) / n,
        aesthetic=sum(v.ratings.aesthetic for v in vectors) / n,
        psychological=sum(v.ratings.psychological for v in vectors) / n,
        epistemic=sum(v.ratings.epistemic for v in vectors) / n,
    )
