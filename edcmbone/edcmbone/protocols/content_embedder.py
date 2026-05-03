from typing import Protocol, Sequence, NamedTuple


class StatusFlags(NamedTuple):
    """Categorical claims about a proposition's logical/evidential structure."""
    truth_status: str         # true | untrue | unknown
    verification_status: str  # verified | unverified | unverifiable
    foundation_status: str    # axiom | derivation | asserted_without_foundation
    speech_act: str           # uttered | referenced | quoted | implied | negated | hypothetical


class ContentRatings(NamedTuple):
    """Scalar quality ratings, receiver-relative and conversation-scoped. Range [0, 1]."""
    utility: float
    clarity: float
    focus: float
    aesthetic: float
    psychological: float
    epistemic: float  # knowledge-quality of the assertion; independent of status flags


class ContentVector(NamedTuple):
    """10D content vector for a single claim (4 status flags + 6 ratings)."""
    status: StatusFlags
    ratings: ContentRatings


class ContentEmbedder(Protocol):
    """Embed a claim into the 10D content space.

    Bone context is provided so the embedder can detect scaffold/fill
    divergence: the bones structure the claim; the flesh fills it.
    The divergence between those two is the primary chicanery signal
    and flows through the bridge layer (O↔B↔C).

    Ratings are receiver-relative and conversation-scoped.
    Status flags describe the proposition's logical/evidential structure.
    The epistemic rating is independent of the three status flags —
    it measures knowledge-quality of the assertion itself.
    """

    def embed(
        self,
        claim: object,
        bone_context: Sequence[object],
    ) -> ContentVector:
        """Produce the 10D status+rating vector for a claim.
        bone_context carries the operator-layer framing of the same region,
        enabling detection of scaffold/fill divergence.
        """
        ...
