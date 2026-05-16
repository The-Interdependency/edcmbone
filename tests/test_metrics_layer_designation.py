from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from edcmbone.metrics import compute
from core.operator import operator_extractor


def test_metrics_compute_is_behavioral_orchestration_not_operator_l0():
    assert compute.LAYER_DECISION == "A_BEHAVIORAL_ORCHESTRATION"
    assert compute.OPERATES_ON_OPERATOR_BONES is False
    assert compute.CONSUMES_BONE_COUNT_FOR_AUDIT is True
    assert compute.OPERATOR_LAYER_SUBSTRATE == "bones_only"
    assert compute.MIGRATION_TARGET == "edcm"


def test_operator_entrypoint_remains_separate_from_metrics_compute():
    assert compute.OPERATOR_ENTRYPOINT == "core.operator.operator_extractor"
    assert hasattr(operator_extractor, "compute_operator_for_turn")
    assert hasattr(operator_extractor, "compute_per_turn_operator")
    assert hasattr(operator_extractor, "compute_operator_windows")


def test_metrics_compute_exposes_upper_layer_vector_shape():
    sample = compute.RoundMetrics(C=1, R=2, F=3, E=4, D=5, N=6, I=7, O=8, L=9, P=10, kappa=11)
    assert sample.vector() == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    assert "bone_count" in sample.as_dict()
