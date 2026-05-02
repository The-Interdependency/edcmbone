from typing import Protocol, Sequence, Tuple, NamedTuple


class DiskCoords(NamedTuple):
    """Per-disk coordinates on the unit hypercircle cross-section."""
    angular: Tuple[float, ...]  # multi-dimensional; n fixed by UCNS implementation
    residue: float
    rotation: float
    chirality: float  # orientation relative to the Möbius twist; flips at zero
    local_relation: float


class CylindricalCoords(NamedTuple):
    """Cross-disk coordinates along the hypercylinder's traversal axis."""
    depth: int  # z in {0, 1, 2, 3}
    sequence_position: int
    recurrence: float
    phase_memory: float
    traversal_index: int


class BoneEmbedding(NamedTuple):
    """Located event on a hyperdisk within the Möbius-cylindrical field.

    The embedding space is Möbius-cylindrical: the edge of each disk is
    Möbius, and the cylinder is Möbius if constructed properly. Zero is
    not the scalar 0.0 — it is the contact event at the Möbius twist,
    the hidden point where orientation flips and from which the field
    unfurls. Chirality is the coordinate that carries this orientation.
    """
    disk: DiskCoords
    cylinder: CylindricalCoords


class BoneEmbedder(Protocol):
    """Protocol for embedding bones into the UCNS Möbius-cylindrical field.

    edcmbone declares this interface. interdependent-lib wires the UCNS
    implementation. No UCNS imports here.

    Mirror symmetry: ghost divisors and phantom products from trailing
    epicycles come in chiral pairs. Solving one chirality resolves its
    mirror by the Möbius symmetry of the cylinder. The distance method
    must account for paths through the twist.
    """

    def embed(self, bone: object, context: Sequence[object]) -> BoneEmbedding:
        """Locate bone as event on a Möbius-cylindrical hyperdisk.
        Context provides neighboring bones for sequence-aware placement.
        """
        ...

    def distance(self, a: BoneEmbedding, b: BoneEmbedding) -> float:
        """Möbius-geodesic distance between two bone embeddings.
        A path through the Möbius twist may be shorter than a path around.
        """
        ...

    def zero(self) -> BoneEmbedding:
        """The contact event at the Möbius twist — the non-scalar origin.
        Not np.zeros(). The first anchoring event from which the field
        unfurls. Chirality at zero is the orientation anchor.
        """
        ...
