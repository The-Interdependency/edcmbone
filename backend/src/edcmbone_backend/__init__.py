"""MSDMD-compliant UCNS-only backend.

The backend models the smallest useful EDCM boundary surface:
constraints are recorded as UCNS-backed boundary objects, and unresolved work is
carried forward in a mandatory ``hmmm`` object instead of being erased.
"""

# === MODULE_BUILD ===
# id: edcmbone_backend_ucns_boundary
#   module_name: edcmbone_backend
#   module_kind: backend
#   summary: UCNS-only backend that records delivered output and unresolved constraints as explicit hmmm boundary objects
#   owner: The Interdependency
#   public_surface: BoundaryObject,Hmmm,make_boundary,merge_boundaries,serialize_boundary,hmmm
#   internal_surface: _coerce_text,_anchor
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: caller supplied text only; no persistence
#   admin_only: false
#   tests: tests.test_backend_contracts
#   rollout: default_enabled
#   rollback: restore backend_old as backend
#   requires: ucns
#   since: 2026-06-25
#   unresolved: The requested The-Interdependency/skill-lib path was not present in this checkout; local .agents/skills was used as the msdmd/test-build source.
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: backend_imports_only_ucns
#   given: the new backend package source is inspected
#   then:  its only import statement imports ucns
#   class: architecture
#   call:  tests.test_backend_contracts.test_backend_imports_only_ucns
#
# id: hmmm_preserves_unresolved_constraint
#   given: a boundary is created with delivered output and an unresolved constraint
#   then:  hmmm is an object and keeps the unresolved text intact
#   class: correctness
#   call:  tests.test_backend_contracts.test_hmmm_preserves_unresolved_constraint
#
# id: hmmm_fallback_is_never_empty
#   given: a boundary is created without an explicit unresolved constraint
#   then:  hmmm still records an honest continuation marker
#   class: correctness
#   call:  tests.test_backend_contracts.test_hmmm_fallback_is_never_empty
#
# id: boundary_objects_are_ucns_backed
#   given: a boundary is created or merged
#   then:  each boundary carries a normalized UCNS object and merged boundaries multiply their UCNS carriers
#   class: correctness
#   call:  tests.test_backend_contracts.test_boundary_objects_are_ucns_backed
# === END CONTRACTS ===

import ucns

__version__ = "0.2.0"


class Hmmm:
    """Mandatory unresolved-continuation boundary object."""

    __slots__ = ("unresolved", "transition", "note")

    def __init__(self, unresolved=None, note=None):
        self.unresolved = _coerce_text(unresolved)
        self.transition = "hmmm"
        self.note = _coerce_text(note) or "the kettle has opinions about incomplete specifications."

    def __bool__(self):
        return True

    def __str__(self):
        if self.unresolved:
            return self.unresolved
        return f"{self.transition}: {self.note}"

    def as_dict(self):
        return {
            "transition": self.transition,
            "unresolved": self.unresolved,
            "note": self.note,
            "text": str(self),
        }


class BoundaryObject:
    """Mandatory boundary object between delivered output and continuation.

    ``hmmm`` is deliberately concrete: unresolved constraints are data, not an
    absence.  The UCNS carrier makes each boundary structurally comparable and
    composable without importing any non-UCNS backend dependency.
    """

    __slots__ = ("delivered", "hmmm", "ucns_object")

    def __init__(self, delivered, hmmm, ucns_object):
        self.delivered = _coerce_text(delivered)
        self.hmmm = hmmm if isinstance(hmmm, Hmmm) else Hmmm(hmmm, "unresolved continuation is present, even when quiet.")
        self.ucns_object = ucns_object.normalize()

    def as_dict(self):
        return {
            "delivered": self.delivered,
            "hmmm": self.hmmm.as_dict(),
            "ucns": {
                "n_dec": self.ucns_object.n_dec,
                "n_min": self.ucns_object.n_min,
                "anchors": [str(anchor.theta) for anchor in self.ucns_object.anchors_pos],
                "faces": list(self.ucns_object.faces_pos),
            },
        }


def _coerce_text(value):
    if value is None:
        return ""
    return str(value).strip()


def _anchor(face):
    return ucns.UCNSObject(
        n_dec=2,
        n_min=1,
        anchors_pos=(ucns.AnchorPayload(0, None),),
        faces_pos=(int(face) & 1,),
    )


def hmmm(unresolved=None):
    """Return the mandatory unresolved-continuation object."""
    return Hmmm(unresolved)


def make_boundary(delivered, unresolved=None):
    """Create a UCNS-backed boundary object from delivered and unresolved text."""
    unresolved_text = _coerce_text(unresolved)
    return BoundaryObject(delivered, hmmm(unresolved_text), _anchor(0 if unresolved_text else 1))


def merge_boundaries(left, right):
    """Compose two boundaries while preserving both delivered and hmmm text."""
    unresolved = "\n".join(text for text in (left.hmmm.unresolved, right.hmmm.unresolved) if text)
    return BoundaryObject(
        "\n".join(part for part in (left.delivered, right.delivered) if part),
        hmmm(unresolved),
        ucns.multiply(left.ucns_object, right.ucns_object),
    )


def serialize_boundary(boundary):
    """Return a JSON-ready dict without importing json."""
    return boundary.as_dict()


__all__ = [
    "BoundaryObject",
    "Hmmm",
    "hmmm",
    "make_boundary",
    "merge_boundaries",
    "serialize_boundary",
]
