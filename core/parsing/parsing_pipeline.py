# core/parsing/parsing_pipeline.py
# hmmm: orchestrates utterances -> turns -> rounds (no IO).

from __future__ import annotations

from typing import Any, Dict, List, Tuple
from .turn_builder import build_turns_from_utterances
from .round_builder import build_rounds_from_turns

def parse_utterances_to_turns_rounds(
    raw_utterances: List[Dict[str, Any]],
    *,
    exclude_sys_tool_from_rounds: bool = True,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    turns = build_turns_from_utterances(raw_utterances)
    rounds = build_rounds_from_turns(turns, exclude_sys_tool_from_rounds=exclude_sys_tool_from_rounds)
    return turns, rounds
