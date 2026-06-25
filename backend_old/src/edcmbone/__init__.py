__version__ = "0.1.0"

from .canon import CanonLoader
from .parser import parse_transcript, ParsedTranscript, Turn, Round, BoneToken, FleshToken
from .metrics import (
    RoundMetrics, compute_round, compute_transcript, energy_step,
    tokenize, ngrams, ttr, repetition_ratio, shannon_entropy,
    novelty, cosine_sim, rep_ngram_density, pattern_density,
    jaccard, correction_fidelity, clamp, norm_per_100,
    fixation_risk, broken_return, escalation_risk, stagnation_risk, loop_risk,
    AgentMetrics, project, project_transcript, gini_tbf,
    fire_alerts, crosswalk_risk,
    A_MATRIX, PROJECTION_MAP, ALERT_THRESHOLDS, RISK_TO_ALERT,
    MATRIX_VERSION, freeze, diff,
)

__all__ = [
    "__version__",
    # Canon
    "CanonLoader",
    # Parser
    "parse_transcript", "ParsedTranscript", "Turn", "Round", "BoneToken", "FleshToken",
    # Metrics — compute
    "RoundMetrics", "compute_round", "compute_transcript", "energy_step",
    # Metrics — stats
    "tokenize", "ngrams", "ttr", "repetition_ratio", "shannon_entropy",
    "novelty", "cosine_sim", "rep_ngram_density", "pattern_density",
    "jaccard", "correction_fidelity", "clamp", "norm_per_100",
    # Metrics — risk
    "fixation_risk", "broken_return", "escalation_risk", "stagnation_risk", "loop_risk",
    # Metrics — projection
    "AgentMetrics", "project", "project_transcript", "gini_tbf",
    "fire_alerts", "crosswalk_risk",
    # Metrics — matrix
    "A_MATRIX", "PROJECTION_MAP", "ALERT_THRESHOLDS", "RISK_TO_ALERT",
    "MATRIX_VERSION", "freeze", "diff",
]
