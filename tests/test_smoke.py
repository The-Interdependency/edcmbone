# tests/test_smoke.py
# hmmm: smoke test = prove the full deterministic pipeline runs end-to-end.

from __future__ import annotations

import json
from pathlib import Path

# Import your engine (repo root assumed on PYTHONPATH when running: python -m tests.test_smoke)
from engine import analyze_transcript, EngineConfig


def main() -> None:
    # Minimal 2-actor transcript (utterances)
    raw_utterances = [
        {"utterance_id": "u0", "actor_id": "A", "raw_text": "We need to decide this now. Do you agree?"},
        {"utterance_id": "u1", "actor_id": "B", "raw_text": "I can't. Not like that. Why are we rushing?"},
        {"utterance_id": "u2", "actor_id": "A", "raw_text": "Because if we don't, it will fail."},
        {"utterance_id": "u3", "actor_id": "B", "raw_text": "Okay. But only if we define the scope."},
        {"utterance_id": "u4", "actor_id": "A", "raw_text": "Agreed. Let's define scope and thresholds."},
        {"utterance_id": "u5", "actor_id": "B", "raw_text": "***"},
        {"utterance_id": "u6", "actor_id": "B", "raw_text": "Also: I won't accept semantic inference in Operator."},
        {"utterance_id": "u7", "actor_id": "A", "raw_text": "Understood. Bones-only stays bones-only."},
    ]

    cfg = EngineConfig(
        canon_dir=Path("canon_eng"),
        validate_with_jsonschema=False,  # set True if you have jsonschema installed
        operator_k_turns=8,
        behavioral_m_rounds=4,
        stride=1,
        divergence_threshold=0.20,
    )

    out = analyze_transcript(raw_utterances, cfg=cfg)

    # Print a quick human sanity summary
    turns = out["turns"]
    rounds = out["rounds"]
    op = out["operator"]
    beh = out["behavioral"]
    br = out["bridge"]

    print("\n=== EDCMBone Smoke Test ===")
    print(f"Turns: {len(turns)}")
    print(f"Rounds: {len(rounds)} (closed={sum(1 for r in rounds if r.get('status')=='closed')}, open={sum(1 for r in rounds if r.get('status')=='open')})")
    print(f"Operator windows: {len(op)} | Behavioral windows: {len(beh)} | Bridge windows: {len(br)}")

    if op:
        v = op[0]["vector"]
        print(f"\nOperator[0] vector (P,K,Q,T,S,sum): {v.get('P'):.3f} {v.get('K'):.3f} {v.get('Q'):.3f} {v.get('T'):.3f} {v.get('S'):.3f} sum={v.get('sum'):.3f}")

    if beh:
        m = beh[0]["metrics"]
        print("\nBehavioral[0] metrics:")
        print(" ".join([f"{k}={m[k]:.3f}" for k in ["C","R","D","N","L","O","F","E","I"]]))

    if br:
        divs = br[-1].get("divergences", [])
        print(f"\nBridge last divergences: {len(divs)}")
        for d in divs[:3]:
            print(f" - {d.get('type')} @ {d.get('round_id')}")

    # Write artifact
#    artifacts = Path("tests/_artifacts")
 #   artifacts.mkdir(parents=True, exist_ok=True)
  #  out_path = artifacts / "smoke_output.json"
   # out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
   # print(f"\nWrote full output JSON to: {out_path}\n")

# hmmm: write artifact relative to THIS file, not CWD (prevents empty/ghost files)
    artifacts = Path(__file__).resolve().parent / "_artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    out_path = artifacts / "smoke_output.json"
    payload = json.dumps(out, indent=2, ensure_ascii=False)

    out_path.write_text(payload, encoding="utf-8")
    print(f"\nWrote full output JSON to: {out_path} ({out_path.stat().st_size} bytes)\n")

    assert out_path.stat().st_size > 10, "Artifact file unexpectedly tiny/empty"

    # Hard failure conditions for smoke test
    assert len(turns) > 0, "No turns produced"
    assert len(rounds) > 0, "No rounds produced"
    assert len(op) > 0, "No operator windows produced"
    assert len(beh) > 0, "No behavioral windows produced"
    assert len(br) > 0, "No bridge windows produced"


if __name__ == "__main__":
    main()
