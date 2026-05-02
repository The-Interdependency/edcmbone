from typing import Protocol, Sequence, NamedTuple, Tuple
from .bone_embedder import BoneEmbedding


class TranscriptEmbedding(NamedTuple):
    """Full depth-3 UCNS embedding of a transcript.

    The three EDCM measurement layers are UCNS recursion depths:
      depth 1 = bones (operator layer, closed-class words and affixes)
      depth 2 = markers (behavioral layer, curated phrasal patterns)
      depth 3 = content (flesh layer, open-class claims)

    A single depth-3 UCNS embedding of a transcript yields all three.
    The Mobius twist is the reference point from which all positions
    in the embedding are measured.
    """
    bone_embeddings: Tuple[BoneEmbedding, ...]   # depth-1 layer
    marker_embeddings: Tuple[BoneEmbedding, ...] # depth-2 layer: bones-within-markers
    content_spans: Tuple[object, ...]            # depth-3 layer: flesh spans


class TranscriptEmbedder(Protocol):
    """Embed a full transcript at depth 3 using the UCNS Mobius-cylindrical field.

    Prerequisite: the UCNS implementation must contain the full bone canon
    from edcmbone bones_v1.json. The current UCNS does not — this is a
    known blocker for correct depth-1 and depth-2 embeddings.

    Pipeline:
      1. Extract bones (depth 1) -> bone_embeddings
      2. Identify markers (deterministic pattern match) ->
         embed each marker as depth-2 UCNS object (bones-within-marker)
      3. Extract content spans (depth 3) -> guided by bone/marker structure

    Claims emerge from depth-2 + depth-3 together:
    markers qualify and characterize; content fills the substance.
    Chicanery is scaffold/fill divergence across all three depths.
    """

    def embed(self, transcript: str) -> TranscriptEmbedding:
        """Produce the full depth-3 embedding of a transcript."""
        ...

    def zero(self) -> BoneEmbedding:
        """The Mobius twist reference point for this transcript embedding."""
        ...
