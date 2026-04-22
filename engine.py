# engine.py
# GPT generated; context, prompt Erin Spencer
# EDCMBone v1.0.0 library engine (framework-agnostic).
# hmmm: This file orchestrates; it must not “improve” canon—only consume it.

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Optional schema validation (recommended)
try:
    import jsonschema  # type: ignore
except Exception:
    jsonschema = None


# ----------------------------
# Config
# ----------------------------

@dataclass(frozen=True)
class EngineConfig:
    canon_dir: Path = Path("canon_eng")
    validate_with_jsonschema: bool = True

    # Window defaults (should align to canon; override only via explicit config)
    operator_k_turns: int = 8
    behavioral_m_rounds: int = 4
    stride: int = 1

    # Bridge defaults
    divergence_threshold: float = 0.20  # default frozen; adjustable


# ----------------------------
# Canon loading + validation
# ----------------------------

def _load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def _validate(schema: Dict[str, Any], obj: Dict[str, Any], name: str) -> None:
    if jsonschema is None:
        return
    jsonschema.validate(instance=obj, schema=schema)

def load_canon(cfg: EngineConfig) -> Dict[str, Any]:
    """
    Loads canon artifacts from canon_dir. Does not mutate them.
    """
    cdir = cfg.canon_dir
    if not cdir.exists():
        raise FileNotFoundError(f"canon_dir not found: {cdir.resolve()}")

    canon = {
        "bones": _load_json(cdir / "bones_v1.json"),
        "affixes": _load_json(cdir / "affixes_v1.json"),
        "behavioral_markers": _load_json(cdir / "behavioral_markers_v1.json"),

        "schemas": {
            "actor": _load_json(cdir / "actor_schema_v1.json"),
            "utterance": _load_json(cdir / "utterance_schema_v1.json"),
            "turn": _load_json(cdir / "turn_schema_v1.json"),
            "round": _load_json(cdir / "round_schema_v1.json"),
            "operator": _load_json(cdir / "operator_schema_v1.json"),
            "behavioral": _load_json(cdir / "behavioral_schema_v1.json"),
            "bridge": _load_json(cdir / "bridge_schema_v1.json"),
        }
    }
    return canon


# ----------------------------
# Public API
# ----------------------------

def analyze_transcript(
    raw_utterances: List[Dict[str, Any]],
    *,
    cfg: Optional[EngineConfig] = None,
) -> Dict[str, Any]:
    """
    Top-level deterministic pipeline:
      utterances -> turns -> rounds -> operator -> behavioral -> bridge

    Inputs:
      raw_utterances: list[Utterance-like dicts] (must include actor_id + raw_text at minimum)

    Output:
      { "turns": [...], "rounds": [...], "operator": {...}, "behavioral": {...}, "bridge": {...} }
    """
    cfg = cfg or EngineConfig()
    canon = load_canon(cfg)

    # ---- Import core components (implement these modules in edcmbone/core/...) ----
    # hmmm: keep these pure; no IO; no global state.
    from core.parsing.parsing_pipeline import parse_utterances_to_turns_rounds
    from core.parsing.round_builder import _is_sys_tool
    from core.operator.operator_extractor import compute_operator_windows, compute_per_turn_operator_outputs
    from core.behavioral.behavioral_window import compute_behavioral_windows
    from core.bridge.bridge_engine import compute_bridge_windows

    # ---- Parse ----
    turns, rounds = parse_utterances_to_turns_rounds(
        raw_utterances,
        exclude_sys_tool_from_rounds=True,
    )

    if cfg.validate_with_jsonschema and jsonschema is not None:
        # validate each turn/round object (best-effort; can be slow)
        turn_schema = canon["schemas"]["turn"]
        round_schema = canon["schemas"]["round"]
        for t in turns:
            _validate(turn_schema, t, "turn")
        for r in rounds:
            _validate(round_schema, r, "round")

    # ---- Operator (turn-native; SYS/TOOL excluded per canon windowing_policy) ----
    # Per canon, SYS/TOOL turns are excluded from Operator by default.
    op_turns = [t for t in turns if not _is_sys_tool(t["actor_id"])]
    per_turn_op_outputs = compute_per_turn_operator_outputs(
        turns=op_turns,
        bones_inventory=canon["bones"],
        affixes_inventory=canon["affixes"],
    )
    operator_outputs = compute_operator_windows(
        turns=op_turns,
        bones_inventory=canon["bones"],
        affixes_inventory=canon["affixes"],
        k_turns=cfg.operator_k_turns,
        stride=cfg.stride,
    )

    if cfg.validate_with_jsonschema and jsonschema is not None:
        op_schema = canon["schemas"]["operator"]
        for o in operator_outputs:
            _validate(op_schema, o, "operator")

    # ---- Behavioral (round-native; closed rounds only by default) ----
    behavioral_outputs = compute_behavioral_windows(
        rounds=rounds,
        turns=turns,
        markers_inventory=canon["behavioral_markers"],
        m_rounds=cfg.behavioral_m_rounds,
        stride=cfg.stride,
        closed_rounds_only=True,
    )

    if cfg.validate_with_jsonschema and jsonschema is not None:
        beh_schema = canon["schemas"]["behavioral"]
        for b in behavioral_outputs:
            _validate(beh_schema, b, "behavioral")

    # ---- Bridge (observational alignment; thresholds adjustable) ----
    bridge_outputs = compute_bridge_windows(
        rounds=rounds,
        turns=turns,
        operator_outputs=operator_outputs,
        per_turn_operator_outputs=per_turn_op_outputs,
        behavioral_outputs=behavioral_outputs,
        divergence_threshold=cfg.divergence_threshold,
        closed_rounds_only=True,
    )

    if cfg.validate_with_jsonschema and jsonschema is not None:
        br_schema = canon["schemas"]["bridge"]
        for br in bridge_outputs:
            _validate(br_schema, br, "bridge")

    return {
        "turns": turns,
        "rounds": rounds,
        "operator": operator_outputs,
        "behavioral": behavioral_outputs,
        "bridge": bridge_outputs,
        "hmm": {
            "contained": [
                "Canon is read-only; engine orchestrates only.",
                "Schema validation optional if jsonschema not installed."
            ],
            "deferred": [
                "PCNA/PCTA routing outputs integration (optional)."
            ]
        }
    }
