# core/parsing/round_builder.py
# hmmm: initiator-return round closure, SYS/TOOL exclusion by default.

from __future__ import annotations

from typing import Any, Dict, List

def _is_sys_tool(actor_id: str) -> bool:
    a = (actor_id or "").upper()
    return a == "SYS" or a.startswith("TOOL:")

def build_rounds_from_turns(
    turns: List[Dict[str, Any]],
    *,
    exclude_sys_tool_from_rounds: bool = True,
) -> List[Dict[str, Any]]:
    # Working set optionally excludes SYS/TOOL from round derivation
    idx_map = []  # maps working index -> original turn_id
    work: List[Dict[str, Any]] = []
    for t in turns:
        if exclude_sys_tool_from_rounds and _is_sys_tool(t["actor_id"]):
            continue
        idx_map.append(t["turn_id"])
        work.append(t)

    rounds: List[Dict[str, Any]] = []
    if not work:
        return rounds

    r_idx = 0
    initiator = None
    open_round_turn_ids: List[str] = []

    for i, t in enumerate(work):
        actor = t["actor_id"]
        tid = t["turn_id"]

        if initiator is None:
            initiator = actor
            open_round_turn_ids = [tid]
            continue

        if actor == initiator and open_round_turn_ids:
            # close previous round at i-1 (already accumulated)
            rounds.append({
                "round_id": f"r{r_idx}",
                "initiator_actor_id": initiator,
                "turn_ids": open_round_turn_ids,
                "status": "closed",
                "meta": {
                    "closure_rule": "initiator_return_v1",
                    "excluded_sys_tool": exclude_sys_tool_from_rounds,
                    "notes": [],
                },
            })
            r_idx += 1
            # start new round at current turn (initiator returns)
            initiator = actor
            open_round_turn_ids = [tid]
        else:
            open_round_turn_ids.append(tid)

    # finalize last round
    if open_round_turn_ids:
        rounds.append({
            "round_id": f"r{r_idx}",
            "initiator_actor_id": initiator,
            "turn_ids": open_round_turn_ids,
            "status": "open" if True else "closed",  # default: last may be open
            "meta": {
                "closure_rule": "initiator_return_v1",
                "excluded_sys_tool": exclude_sys_tool_from_rounds,
                "notes": ["status=open because transcript ended before initiator returned"],
            },
        })

    return rounds
