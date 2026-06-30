# ratios: loc_comments=9:6 imports_exports=2:1 calls_definitions=0:1
"""
Content-layer scalar ratings (6 per claim, each in [0, 1]).
Reference frame: receiver-relative, conversation-scoped (provisional default per §3.2).
Source: canon_eng/canon_v2_proposal.md §1.5 and §3.2.
"""
from __future__ import annotations
from typing import NamedTuple


class ContentRatings(NamedTuple):
    """6D scalar rating vector for a single claim. All values in [0, 1]."""
    utility: float       # value to the receiver in this conversation’s context
    clarity: float       # intelligibility to the receiver
    focus: float         # relevance to the conversation’s stated topic
    aesthetic: float     # form quality (0 = poor, 1 = excellent)
    psychological: float # appropriateness for the receiver
    epistemic: float     # knowledge-quality: warranted, well-grounded, hedged
# ratios: loc_comments=9:6 imports_exports=2:1 calls_definitions=0:1
