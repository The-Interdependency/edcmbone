"""
Behavioral snapshot marker engine.
Implements behavioral_markers_v1.json (frozen v1.0.0) pattern matching.

Tier A: structural phrase and pattern matching (preferred).
Tier B: lexical anchor matching (minimal; intended for replacement in v2).

All pattern inventories are inlined from the frozen canon.
Zero external dependencies; stdlib only.
"""
from __future__ import annotations
from typing import NamedTuple


# ── Tier A inventories ─────────────────────────────────────────────────────
# Source: canon_eng/behavioral_markers_v1.json, frozen v1.0.0

# C — Constraint Strain
_C_NEGATION = {"not", "no", "never", "n't"}
_C_CONTRAST = {"but", "however", "though", "although", "yet", "instead", "otherwise"}
_C_CF_MODALS = {"would", "could", "might", "should"}
_C_HARD_MODALS = {"must", "have to", "need to"}
_C_HARD_NEG = {"can't", "cannot", "won't", "not"}
_C_TIER_B = {"contradict", "inconsistent", "doesn't add up", "makes no sense", "impossible"}

# R — Refusal Density
_R_HARD = [
    "i can't", "i cannot", "can't", "cannot", "won't", "will not",
    "i won't", "not allowed", "against policy", "unable to", "i'm unable",
    "i refuse", "refuse to",
]
_R_SOFT = [
    "i don't know", "not sure", "i'm not sure", "unclear",
    "i can't help with that", "i can't do that",
]
_R_TIER_B = ["policy", "disallowed", "prohibited"]

# D — Deflection
_D_SHIFT = [
    "anyway", "regardless", "moving on", "let's", "by the way", "in other news",
]
_D_META = [
    "as an ai", "i can't browse", "i don't have access", "i can't see",
]
_D_TIER_B = ["unrelated", "separately", "different topic"]

# N — Noise
_N_ACTION = [
    "steps:", "1)", "2)", "3)", "- ", "* ",
    "do this", "try this", "run", "install", "set", "change", "use", "add", "remove",
]
_N_PADDING = [
    "in general", "typically", "often", "usually", "it depends",
    "broadly", "overall",
]
_N_TIER_B = ["philosophically", "metaphorically", "abstractly"]

# L — Load
_L_MODALS = ["must", "need", "have to", "required", "can't", "cannot", "should"]
_L_COND = ["if", "unless", "until"]
_L_DELIM = ["only", "exactly", "no", "not"]
_L_TIER_B = ["constraint", "requirement", "rule", "canon", "frozen"]

# O — Overextension
_O_EXPAND = [
    "also", "additionally", "furthermore", "another", "moreover",
    "we can", "we could", "next", "in addition",
]
_O_TIER_B = ["scope", "expand", "overreach", "extra"]

# F — Fixation (proxy: repeat-rate of constraint tokens)
_F_PROXY_TOKENS = set(_L_MODALS) | {"constraint", "rule", "canon", "frozen"}
_F_TIER_B = ["again", "still", "same", "repeat"]

# E — Escalation
_E_INTENSITY = [
    "must", "no choice", "unacceptable", "absolutely", "under no circumstance",
    "immediately", "now", "stop", "never",
]
_E_PUNCT = ["!!", "!!!"]
_E_TIER_B = ["escalate", "urgent", "crisis"]

# I — Integration Failure
_I_CORRECTION = [
    "no", "that's wrong", "incorrect", "not what i meant", "you missed",
    "fix", "revise", "update", "remove", "stop",
]
_I_ACK = [
    "you're right", "correct", "my mistake", "apologies", "i'll fix",
    "updated", "revised",
]
_I_TIER_B = ["incorporate", "align", "consistent"]


# ── Matching helpers ─────────────────────────────────────────────────────

def _count_phrases(text: str, phrases: list[str]) -> int:
    """Count distinct phrase hits (substring, case-insensitive)."""
    return sum(1 for p in phrases if p in text)


def _count_tokens(text: str, tokens: set[str]) -> int:
    """Count word-boundary token hits (whitespace tokenization, lowercase)."""
    words = set(text.split())
    return len(words & tokens)


def _question_count(text: str) -> int:
    return text.count("?")


# ── Per-turn raw scores ─────────────────────────────────────────────────────

class TurnScores(NamedTuple):
    """Raw (unnormalized) marker hit scores for a single turn."""
    C_negation_contrast: float    # C.A.01
    C_question_pressure: float    # C.A.02
    C_modal_collision: float      # C.A.03
    C_tier_b: float
    R_hard: float
    R_soft: float
    R_tier_b: float
    D_shift: float
    D_meta: float
    D_tier_b: float
    N_action: float
    N_padding: float
    N_tier_b: float
    L_modal: float
    L_cond: float
    L_delim: float
    L_tier_b: float
    O_expand: float
    O_tier_b: float
    F_proxy: float                # repeat-rate proxy: raw constraint token count
    F_tier_b: float
    E_intensity: float
    E_punct: float
    E_tier_b: float
    I_correction: float
    I_ack: float
    I_tier_b: float


def score_turn(text: str) -> TurnScores:
    """
    Compute raw marker hit scores for a single turn text.
    All scores are raw hit counts; normalization happens in metrics.py.
    """
    t = text.lower()
    words = set(t.split())

    # C
    neg_present = bool(_C_NEGATION & words)
    contrast_present = bool(_C_CONTRAST & words)
    cf_modal_present = bool(_C_CF_MODALS & words)
    hard_modal = bool(any(m in t for m in _C_HARD_MODALS))
    hard_neg = bool(any(m in t for m in _C_HARD_NEG))
    C_neg_contrast = 0.70 if (neg_present and contrast_present) else 0.0
    C_qp = 0.35 * min(_question_count(t), 5)
    C_mc = 0.85 if (hard_modal and hard_neg) else 0.0
    C_tb = 0.75 * _count_phrases(t, _C_TIER_B)

    # R
    R_hard = 1.0 * _count_phrases(t, _R_HARD)
    R_soft = 0.5 * _count_phrases(t, _R_SOFT)
    R_tb = 0.75 * _count_phrases(t, _R_TIER_B)

    # D
    D_shift = _count_phrases(t, _D_SHIFT)
    D_meta = _count_phrases(t, _D_META)
    D_tb = 0.60 * _count_phrases(t, _D_TIER_B)

    # N
    N_action = 1.0 * _count_phrases(t, _N_ACTION)
    N_pad = 0.5 * _count_phrases(t, _N_PADDING)
    N_tb = 0.50 * _count_phrases(t, _N_TIER_B)

    # L
    L_modal = 1.0 * sum(1 for m in _L_MODALS if m in t)
    L_cond = 0.6 * sum(1 for m in _L_COND if m in words)
    L_delim = 0.6 * sum(1 for m in _L_DELIM if m in words)
    L_tb = 0.75 * _count_phrases(t, _L_TIER_B)

    # O
    O_exp = _count_phrases(t, _O_EXPAND)
    O_tb = 0.60 * _count_phrases(t, _O_TIER_B)

    # F (proxy: raw count of constraint-proxy tokens for repeat-rate computation)
    F_proxy = float(_count_tokens(t, _F_PROXY_TOKENS))
    F_tb = _count_phrases(t, _F_TIER_B)

    # E
    E_int = sum(1 for m in _E_INTENSITY if m in t)
    E_punct = sum(1 for p in _E_PUNCT if p in text)  # preserve original case for !
    E_tb = 0.60 * _count_phrases(t, _E_TIER_B)

    # I
    I_corr = _count_phrases(t, _I_CORRECTION)
    I_ack = _count_phrases(t, _I_ACK)
    I_tb = 0.50 * _count_phrases(t, _I_TIER_B)

    return TurnScores(
        C_negation_contrast=C_neg_contrast,
        C_question_pressure=C_qp,
        C_modal_collision=C_mc,
        C_tier_b=C_tb,
        R_hard=R_hard,
        R_soft=R_soft,
        R_tier_b=R_tb,
        D_shift=float(D_shift),
        D_meta=float(D_meta),
        D_tier_b=D_tb,
        N_action=N_action,
        N_padding=N_pad,
        N_tier_b=N_tb,
        L_modal=L_modal,
        L_cond=L_cond,
        L_delim=L_delim,
        L_tier_b=L_tb,
        O_expand=float(O_exp),
        O_tier_b=O_tb,
        F_proxy=F_proxy,
        F_tier_b=float(F_tb),
        E_intensity=float(E_int),
        E_punct=float(E_punct),
        E_tier_b=E_tb,
        I_correction=float(I_corr),
        I_ack=float(I_ack),
        I_tier_b=I_tb,
    )
