from typing import Protocol, Sequence, NamedTuple


class Claim(NamedTuple):
    """A single extracted claim with its bone-determined structural type.

    Bones reveal the claim scaffold (assertion, hedge, negation,
    conditionality, reframe). Flesh fills the content slots.
    The scaffold is bone-determined; the content is flesh-determined.
    """
    bone_structure: object        # bone parse sequence framing this claim
    speech_act: str               # uttered | referenced | quoted | implied | negated | hypothetical
    foundation_status: str        # axiom | derivation | asserted_without_foundation
    flesh_text: str               # open-class content filling the bone scaffold
    span_start: int
    span_end: int


class ClaimExtractor(Protocol):
    """Extract claims from text using bone structure as scaffold.

    Works bone-first, not NLP-first. Bone patterns identify the structural
    type of each claim region; flesh extraction fills the content slots.

    Chicanery signal: divergence between what the bone scaffold frames
    and what the flesh content asserts. That divergence is reported
    through the bridge layer (O↔B↔C), not manufactured here.
    """

    def extract(
        self,
        text: str,
        bone_parse: Sequence[object],
    ) -> Sequence[Claim]:
        """Extract claims from text.
        bone_parse is the operator-layer output for the same text.
        Bone patterns determine speech_act and foundation_status;
        flesh_text is the open-class content within each claim boundary.
        """
        ...
