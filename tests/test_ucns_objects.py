"""UCNS construction-object tests for the v0.2 metric-orthogonality spec.

Covers ConstraintField / FieldMotion readouts and the spec §14 obligations:
empty field -> NA (not 0), signed-ternary states, F/E/O_scope share a parent
hash with distinct axis ids, and the §13 F/E/O_scope fixture matrix.
"""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"


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
ConstraintField = orthogonality.ConstraintField
FieldMotion = orthogonality.FieldMotion
canonical_axes = orthogonality.canonical_axes
FIELD_MOTION_FIXTURE_MATRIX = orthogonality.FIELD_MOTION_FIXTURE_MATRIX
field_motion_fixture = orthogonality.field_motion_fixture


def test_empty_field_readouts_are_na_not_zero():
    cf = ConstraintField(grain="round", raised_field_count=0, contact="against")
    assert cf.present is False
    assert cf.contact_state().enabled is False
    assert cf.resolution_state().enabled is False
    for readout in cf.behavioral_readouts().values():
        assert readout.state.enabled is False
        assert readout.state != AxisState(enabled=True, s=0, m=0.0)


def test_contact_direction_maps_to_signed_ternary():
    assert ConstraintField("round", 3, contact="toward").contact_state().s == 1
    assert ConstraintField("round", 3, contact="against").contact_state().s == -1
    assert ConstraintField("round", 3, contact="away").contact_state().s == 0


def test_resolution_state_maps_to_signed_ternary():
    assert ConstraintField("round", 3, resolution="closed").resolution_state().s == 1
    assert ConstraintField("round", 3, resolution="open").resolution_state().s == -1
    assert ConstraintField("round", 3, resolution="unresolved").resolution_state().s == 0


def test_behavioral_readouts_directionality():
    cf = ConstraintField("round", 3, contact="away", resolution="open")
    ro = cf.behavioral_readouts()
    assert ro["edcm.behavioral.D.deflection"].state.s == 1   # away deflects
    assert ro["edcm.behavioral.R.refusal_density"].state.s == 0
    assert ro["edcm.behavioral.I.integration"].state.s == -1  # open constraint
    against = ConstraintField("round", 3, contact="against").behavioral_readouts()
    assert against["edcm.behavioral.R.refusal_density"].state.s == 1
    assert against["edcm.behavioral.L_resistance"].state.s == 1


def test_readouts_share_field_hash_parent():
    cf = ConstraintField("round", 3, contact="against", resolution="open")
    parents = {r.parent_hash for r in cf.behavioral_readouts().values()}
    assert parents == {cf.field_hash}


def test_field_motion_fixture_matrix():
    for name, (f, e, o) in FIELD_MOTION_FIXTURE_MATRIX.items():
        ro = field_motion_fixture(name).readouts()
        assert ro["edcm.behavioral.F.fixation"].state.s == f, name
        assert ro["edcm.behavioral.E.escalation"].state.s == e, name
        assert ro["edcm.behavioral.O_scope"].state.s == o, name


def test_feo_readouts_share_parent_with_distinct_ids():
    fm = field_motion_fixture("runaway_spiral")
    ro = fm.readouts()
    parents = {r.parent_hash for r in ro.values()}
    assert parents == {fm.parent_hash}
    ids = {r.metric_id for r in ro.values()}
    assert ids == {
        "edcm.behavioral.F.fixation",
        "edcm.behavioral.E.escalation",
        "edcm.behavioral.O_scope",
    }


def test_field_motion_na_when_no_field_present():
    fm = FieldMotion("prev", "cur", present=False, recurrence_reads=(1.0,))
    assert fm.fixation().state.enabled is False


def test_projection_registry_complete_and_not_primitive():
    axes = canonical_axes()
    for pid in (
        "edcm.projection.CM",
        "edcm.projection.DA",
        "edcm.projection.DRIFT",
        "edcm.projection.DVG",
        "edcm.projection.INT",
        "edcm.projection.TBF",
    ):
        assert pid in axes
        assert axes[pid].primitive is False
