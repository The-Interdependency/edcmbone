# core/parsing/turn_builder.py
# hmmm: turn merge doctrine + forced boundary markers.

from __future__ import annotations

from typing import Any, Dict, List, Optional
from .tokenizer import tokens_surface

BOUNDARY_MARKERS = {"***", "[break]", "[pause]", "[header]", "---"}

def _is_forced_boundary(raw_text: str) -> bool:
    t = (raw_text or "").strip().lower()
    return t in BOUNDARY_MARKERS

def build_turns_from_utterances(raw_utterances: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    turns: List[Dict[str, Any]] = []

    def new_turn(turn_id: str, actor_id: str) -> Dict[str, Any]:
        return {
            "turn_id": turn_id,
            "actor_id": actor_id,
            "utterance_ids": [],
            "raw_text": "",
            "tokens_surface": [],
            "t_start": None,
            "t_end": None,
            "source_refs": [],
            "meta": {
                "forced_boundary": False,
                "contains_quote": False,
                "overlap": False,
                "interrupted_by": None,
                "notes": [],
            },
        }

    current: Optional[Dict[str, Any]] = None
    turn_idx = 0

    for i, u in enumerate(raw_utterances):
        actor = u.get("actor_id") or "UNK"
        utt_id = u.get("utterance_id") or f"u{i}"
        raw = u.get("raw_text") or ""
        src = u.get("source_ref")
        t_start = u.get("t_start")
        t_end = u.get("t_end")

        forced = _is_forced_boundary(raw)
        contains_quote = ('"' in raw)  # frozen: quote detection only by double quote
        overlap = ("[overlap" in raw.lower()) or ("[overlapping" in raw.lower())

        start_new = False
        if current is None:
            start_new = True
        else:
            if forced:
                start_new = True
            elif actor == "UNK" or current["actor_id"] == "UNK":
                # UNK utterances are never merged with neighbours
                start_new = True
            elif actor != current["actor_id"]:
                start_new = True

        if start_new:
            current = new_turn(f"t{turn_idx}", actor)
            turn_idx += 1
            turns.append(current)

        # Merge utterance into current turn
        current["utterance_ids"].append(utt_id)
        if current["raw_text"]:
            # frozen separator: newline between merged utterances
            current["raw_text"] += "\n" + raw
        else:
            current["raw_text"] = raw

        # timestamps: best-effort
        if current["t_start"] is None and t_start is not None:
            current["t_start"] = t_start
        if t_end is not None:
            current["t_end"] = t_end

        if src:
            current["source_refs"].append(str(src))

        # meta
        current["meta"]["forced_boundary"] = current["meta"]["forced_boundary"] or forced
        current["meta"]["contains_quote"] = current["meta"]["contains_quote"] or contains_quote
        current["meta"]["overlap"] = current["meta"]["overlap"] or overlap

    # finalize tokens_surface
    for t in turns:
        t["tokens_surface"] = tokens_surface(t["raw_text"])

    return turns
