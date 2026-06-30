import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend_old" / "src"


def _load_package(package_name: str, package_dir: Path):
    existing = sys.modules.get(package_name)
    if existing is not None:
        return existing

    spec = importlib.util.spec_from_file_location(
        package_name,
        package_dir / "__init__.py",
        submodule_search_locations=[str(package_dir)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[package_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _load_module(module_name: str, module_path: Path):
    existing = sys.modules.get(module_name)
    if existing is not None:
        return existing

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_load_package("edcmbone", BACKEND_SRC / "edcmbone")
_load_package("edcmbone.metrics", BACKEND_SRC / "edcmbone" / "metrics")
compute = _load_module(
    "edcmbone.metrics.compute",
    BACKEND_SRC / "edcmbone" / "metrics" / "compute.py",
)

_load_package("core", ROOT / "core")
_load_package("core.operator", ROOT / "core" / "operator")
operator_extractor = _load_module(
    "core.operator.operator_extractor",
    ROOT / "core" / "operator" / "operator_extractor.py",
)


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
