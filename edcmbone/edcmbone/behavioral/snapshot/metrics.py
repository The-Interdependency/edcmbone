# ratios: loc_comments=73:42 imports_exports=3:2 calls_definitions=38:6
"""
Behavioral snapshot 9D vector.
Aggregates TurnScores over a round window (W_round m=4) into BehavioralSnapshot.
Zero external dependencies; stdlib only.
"""
from __future__ import annotations
from typing import NamedTuple, Sequence
from .markers import TurnScores, score_turn


class BehavioralSnapshot(NamedTuple):
    """
    9D behavioral snapshot vector (frozen v1 metrics).
    All values in [0, 1] after normalization; see per-field notes.
    """
    C: float  # Constraint Strain
    R: float  # Refusal Density
    D: float  # Deflection
    N: float  # Noise (higher = more noise; resolution-action reduces it)
    L: float  # Constraint Load
    O: float  # Overextension
    F: float  # Fixation (repeat-rate proxy)
    E: float  # Escalation
    I: float  # Integration Failure


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, x))


def _f_repeat_rate(proxy_counts: list[float]) -> float:
    """
    Fixation proxy: normalized standard deviation of per-turn constraint
    token counts. High variance = low fixation; low variance = high fixation.
    v1 structural proxy per behavioral_markers_v1.json.
    """
    n = len(proxy_counts)
    if n < 2:
        return 0.0
    mean = sum(proxy_counts) / n
    if mean == 0.0:
        return 0.0
    variance = sum((x - mean) ** 2 for x in proxy_counts) / n
    std = variance ** 0.5
    # High std/mean = low fixation; invert so high F = high fixation
    cv = std / mean  # coefficient of variation
    return _clamp(1.0 - min(cv, 1.0))


def _e_escalation_trend(intensity_counts: list[float]) -> float:
    """
    Escalation trend: positive derivative over window.
    Compare mean of second half vs first half of turns.
    """
    n = len(intensity_counts)
    if n < 2:
        return 0.0
    mid = n // 2
    first = sum(intensity_counts[:mid]) / max(mid, 1)
    second = sum(intensity_counts[mid:]) / max(n - mid, 1)
    delta = second - first
    # Normalize: delta of 3+ intensity markers per turn = maximal escalation
    return _clamp(delta / 3.0)


def score_window(turns: Sequence[str]) -> BehavioralSnapshot:
    """
    Compute the 9D behavioral snapshot vector for a round window.

    turns: sequence of turn texts (caller supplies the closed W_round(m=4) window;
           turns from all participants are included per parsing canon).

    Normalization strategy:
    - C, R, D, L, O, E: sum weighted hits / (n_turns * cap), clamped to [0,1]
    - N: resolution-action density minus padding density
    - F: repeat-rate proxy (std/mean of constraint token counts, inverted)
    - I: correction-without-ack ratio (proxy in v1)
    """
    if not turns:
        return BehavioralSnapshot(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    scored: list[TurnScores] = [score_turn(t) for t in turns]
    n = len(scored)

    def _sum(field: str) -> float:
        return sum(getattr(s, field) for s in scored)

    # C: weighted constraint contradiction density
    C_raw = (_sum("C_negation_contrast") + _sum("C_question_pressure")
             + _sum("C_modal_collision") + _sum("C_tier_b"))
    C = _clamp(C_raw / (n * 3.0))

    # R: refusal density
    R_raw = _sum("R_hard") + _sum("R_soft") + _sum("R_tier_b")
    R = _clamp(R_raw / (n * 2.0))

    # D: deflection ratio
    D_raw = _sum("D_shift") + _sum("D_meta") + _sum("D_tier_b")
    D = _clamp(D_raw / (n * 2.0))

    # N: noise = padding dominates over action
    N_action = _sum("N_action")
    N_pad = _sum("N_padding") + _sum("N_tier_b")
    # High action relative to padding = low noise
    if N_action + N_pad == 0:
        N = 0.0
    else:
        N = _clamp(N_pad / (N_action + N_pad))

    # L: constraint load
    L_raw = _sum("L_modal") + _sum("L_cond") + _sum("L_delim") + _sum("L_tier_b")
    L = _clamp(L_raw / (n * 5.0))

    # O: overextension
    O_raw = _sum("O_expand") + _sum("O_tier_b")
    O = _clamp(O_raw / (n * 3.0))

    # F: fixation via repeat-rate proxy
    F = _f_repeat_rate([s.F_proxy for s in scored])

    # E: escalation trend + base intensity
    E_base = _clamp((_sum("E_intensity") + _sum("E_punct") + _sum("E_tier_b"))
                    / (n * 3.0))
    E_trend = _e_escalation_trend([s.E_intensity for s in scored])
    E = _clamp((E_base + E_trend) / 2.0)

    # I: integration failure proxy
    # Correction markers without subsequent ack = failure
    I_corr = _sum("I_correction")
    I_ack = _sum("I_ack")
    I_tb = _sum("I_tier_b")
    if I_corr == 0:
        I = _clamp(I_tb / (n * 2.0))
    else:
        # High correction with low ack = high I
        ack_ratio = I_ack / (I_corr + 1)
        I = _clamp((1.0 - ack_ratio) * 0.7 + I_tb / (n * 2.0) * 0.3)

    return BehavioralSnapshot(C=C, R=R, D=D, N=N, L=L, O=O, F=F, E=E, I=I)
# ratios: loc_comments=73:42 imports_exports=3:2 calls_definitions=38:6
