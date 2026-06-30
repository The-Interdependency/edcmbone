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
orthogonality = _load_module(
    "edcmbone.metrics.orthogonality",
    BACKEND_SRC / "edcmbone" / "metrics" / "orthogonality.py",
)

AxisState = orthogonality.AxisState
canonical_axes = orthogonality.canonical_axes


def test_na_is_not_zero_state():
    na = AxisState.na()
    zero = AxisState(enabled=True, s=0, m=0.0)
    assert na.enabled is False
    assert zero.enabled is True
    assert na != zero


def test_signed_ternary_enforced():
    AxisState(enabled=True, s=-1, m=0.1)
    AxisState(enabled=True, s=0, m=0.5)
    AxisState(enabled=True, s=1, m=1.0)


def test_o_and_l_axes_are_distinct_and_signed_ids_exist():
    axes = canonical_axes()
    assert "edcm.behavioral.O_scope" in axes
    assert "edcm.behavioral.O_confidence" in axes
    assert axes["edcm.behavioral.O_scope"].metric_id != axes["edcm.behavioral.O_confidence"].metric_id
    assert axes["edcm.behavioral.L_load"].metric_id != axes["edcm.behavioral.L_loss"].metric_id


def test_projection_not_primitive_and_kappa_state_composite_parent():
    axes = canonical_axes()
    assert axes["edcm.projection.CM"].primitive is False
    assert axes["edcm.state.kappa"].parent_object == "state composite"
    assert axes["edcm.round.P_progress"].metric_id != "operator.P"
