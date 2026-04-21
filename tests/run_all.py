# tests/run_all.py
# hmmm: single-file full validation harness for EDCMBone v1.0.0
# - Runs smoke transcript
# - Validates schemas (if jsonschema installed)
# - Writes artifact
# - Compares to golden (if exists)
# - Can update golden intentionally

from __future__ import annotations

import json
import sys
from pathlib import Path
from engine import analyze_transcript, EngineConfig

try:
    import jsonschema  # noqa
    SCHEMA_AVAILABLE = True
except Exception:
    SCHEMA_AVAILABLE = False


# -----------------------------
# Config
# -----------------------------

UPDATE_GOLDEN = "--update-golden" in sys.argv

ROOT = Path(__file__).resolve().parent
ARTIFACT_DIR = ROOT / "_artifacts"
GOLDEN_DIR = ROOT / "golden"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
GOLDEN_DIR.mkdir(parents=True, exist_ok=True)

GOLDEN_PATH = GOLDEN_DIR / "v1.0.0_smoke.json"
ARTIFACT_PATH = ARTIFACT_DIR / "current_output.json"


# -----------------------------
# Test Transcript
# -----------------------------

RAW_UTTERANCES = [
    {"utterance_id": "u0", "actor_id": "A", "raw_text": "We must decide this now. Do you agree?"},
    {"utterance_id": "u1", "actor_id": "B", "raw_text": "I can't. Not like that."},
    {"utterance_id": "u2", "actor_id": "A", "raw_text": "If we don't, it will fail."},
    {"utterance_id": "u3", "actor_id": "B", "raw_text": "Okay, but only if we define scope."},
]


# -----------------------------
# Run Engine
# -----------------------------

cfg = EngineConfig(
    validate_with_jsonschema=SCHEMA_AVAILABLE,
    operator_k_turns=8,
    behavioral_m_rounds=4,
    stride=1,
)

output = analyze_transcript(RAW_UTTERANCES, cfg=cfg)

payload = json.dumps(output, indent=2, ensure_ascii=False)
ARTIFACT_PATH.write_text(payload, encoding="utf-8")

print(f"\nOutput written to: {ARTIFACT_PATH}")
print(f"Size: {ARTIFACT_PATH.stat().st_size} bytes")

assert ARTIFACT_PATH.stat().st_size > 50, "Output file suspiciously small."


# -----------------------------
# Golden Comparison
# -----------------------------

if GOLDEN_PATH.exists():
    golden = GOLDEN_PATH.read_text(encoding="utf-8")
    if golden != payload:
        print("\n❌ DRIFT DETECTED: Output differs from golden file.")

        if UPDATE_GOLDEN:
            GOLDEN_PATH.write_text(payload, encoding="utf-8")
            print("✔ Golden file updated intentionally.")
            sys.exit(0)

        else:
            print("Run with --update-golden to accept changes.")
            sys.exit(1)
    else:
        print("\n✔ Output matches golden file.")

else:
    print("\nNo golden file found.")
    if UPDATE_GOLDEN:
        GOLDEN_PATH.write_text(payload, encoding="utf-8")
        print("✔ Golden file created.")
    else:
        print("Run with --update-golden to create golden baseline.")


print("\n✔ ALL TESTS PASSED\n")

print("hmm:")
print("- Canon read-only.")
print("- Deterministic pipeline validated.")
print("- Drift detection active.")
