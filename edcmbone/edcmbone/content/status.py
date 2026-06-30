# ratios: loc_comments=27:5 imports_exports=3:5 calls_definitions=0:5
"""
Content-layer status flag types (4 categorical per claim).
Source: canon_eng/canon_v2_proposal.md §1.5, frozen pending v2 freeze.
"""
from __future__ import annotations
from enum import Enum
from typing import NamedTuple


class TruthStatus(str, Enum):
    TRUE = "true"
    UNTRUE = "untrue"
    UNKNOWN = "unknown"


class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    UNVERIFIABLE = "unverifiable"


class FoundationStatus(str, Enum):
    AXIOM = "axiom"
    DERIVATION = "derivation"
    ASSERTED_WITHOUT_FOUNDATION = "asserted_without_foundation"


class SpeechAct(str, Enum):
    UTTERED = "uttered"
    REFERENCED = "referenced"
    QUOTED = "quoted"
    IMPLIED = "implied"
    NEGATED = "negated"
    HYPOTHETICAL = "hypothetical"


class StatusFlags(NamedTuple):
    """4-categorical status vector for a single claim."""
    truth_status: TruthStatus
    verification_status: VerificationStatus
    foundation_status: FoundationStatus
    speech_act: SpeechAct
# ratios: loc_comments=27:5 imports_exports=3:5 calls_definitions=0:5
