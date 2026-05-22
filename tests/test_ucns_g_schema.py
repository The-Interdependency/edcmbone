"""Tests for the UCNS-G v3 schema.

Pins the spec-level invariants from
``docs/handoffs/2026-05-22-ucns-g-prime-cylinder-v3.md``:

  * One disk per primitive metric axis, anchored on a prime.
  * Signed ternary axis state {-1, 0, +1}; 0 is neutral, not absence.
  * Twist is ordinal (>= 0), distinct from phase ([0, 1)).
  * Möbius face is -1 or +1.
  * Unit gauge is typed (radius / circumference / area / depth).
  * Grain order is token < turn < round < session < archive.

These tests do not exercise the scalar EDCM metric vector in
``backend/src/edcmbone/metrics/compute.py`` — UCNS-G is additive to the
scalar layer, not a replacement.
"""

import importlib.util
import sys
from fractions import Fraction
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


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


# The root-level `edcmbone/` package is the refactor-in-progress location
# where UCNS-G v3 lives. We load it explicitly rather than via plain
# import so the stable Backend/src/edcmbone package is not shadowed.
_edcmbone_root = _load_package("edcmbone_root_pkg", ROOT / "edcmbone")
ucns_g = _load_package("edcmbone_root_pkg.ucns_g", ROOT / "edcmbone" / "ucns_g")


# ---------------------------------------------------------------------------
# Prime-axis assignment
# ---------------------------------------------------------------------------


def test_prime_axis_assignment_matches_v3_handoff():
    expected = {
        "P": 2, "K": 3, "Q": 5, "T": 7, "S": 11,
        "C": 13, "R": 17, "D": 19, "N": 23, "L": 29,
        "O": 31, "F": 37, "E": 41, "I": 43,
    }
    assert dict(ucns_g.PRIME_AXIS_ASSIGNMENT) == expected


def test_prime_assignment_is_immutable():
    with pytest.raises(TypeError):
        ucns_g.PRIME_AXIS_ASSIGNMENT["P"] = 999  # type: ignore[index]


def test_prime_for_axis_rejects_non_primitive():
    with pytest.raises(KeyError):
        ucns_g.prime_for_axis("Z")


def test_operator_and_metric_axis_partitions_are_disjoint():
    op = set(ucns_g.PRIMITIVE_OPERATOR_AXES)
    me = set(ucns_g.PRIMITIVE_METRIC_AXES)
    assert op.isdisjoint(me)
    assert op | me == set(ucns_g.PRIME_AXIS_ASSIGNMENT.keys())


# ---------------------------------------------------------------------------
# UnitGauge
# ---------------------------------------------------------------------------


def test_unit_gauge_typed_ones_are_distinct():
    r = ucns_g.UnitGauge.one_R()
    c = ucns_g.UnitGauge.one_C()
    a = ucns_g.UnitGauge.one_A()
    z = ucns_g.UnitGauge.one_Z()

    # All display as value 1 ...
    assert r.value == c.value == a.value == z.value == Fraction(1)

    # ... but they are not the same unit basis.
    assert r != c
    assert c != a
    assert a != z
    assert r != z


# ---------------------------------------------------------------------------
# MetricDiskState
# ---------------------------------------------------------------------------


def _mk_state(**overrides):
    base = dict(
        axis="C",
        prime_axis=13,
        grain="turn",
        twist_ordinal=0,
        phase=Fraction(0),
        face=1,
        sign=0,
        magnitude=Fraction(0),
        gauge="radius",
    )
    base.update(overrides)
    return ucns_g.MetricDiskState(**base)


def test_metric_disk_state_constructs_with_valid_inputs():
    s = _mk_state()
    assert s.axis == "C"
    assert s.prime_axis == 13
    assert s.grain == "turn"
    assert s.twist_ordinal == 0
    assert s.phase == Fraction(0)
    assert s.face == 1
    assert s.sign == 0
    assert s.magnitude == Fraction(0)
    assert s.gauge == "radius"
    assert s.confidence is None


def test_metric_disk_state_is_frozen():
    s = _mk_state()
    with pytest.raises(Exception):
        s.phase = Fraction(1, 2)  # type: ignore[misc]


def test_phase_must_be_half_open_unit_interval():
    # 1 should be excluded — phase wraps to twist+1, phase=0.
    with pytest.raises(ValueError):
        _mk_state(phase=Fraction(1))
    with pytest.raises(ValueError):
        _mk_state(phase=Fraction(-1, 8))


def test_twist_ordinal_is_nonnegative_int():
    with pytest.raises(ValueError):
        _mk_state(twist_ordinal=-1)


def test_face_must_be_signed_unit():
    with pytest.raises(ValueError):
        _mk_state(face=0)  # 0 is not a face value


def test_sign_must_be_signed_ternary():
    for s in (-1, 0, 1):
        _mk_state(sign=s)  # valid
    with pytest.raises(ValueError):
        _mk_state(sign=2)


def test_zero_sign_is_neutral_not_absence():
    """Pin: sign=0 is a valid, constructible state.

    The v3 handoff explicitly distinguishes neutral (sign=0) from absent.
    Absence would be 'no disk state at this grain' (i.e. the disk is
    omitted from the grain tensor entirely), not sign=0.
    """
    neutral = _mk_state(sign=0)
    assert neutral.sign == 0


def test_magnitude_must_be_unit_interval():
    with pytest.raises(ValueError):
        _mk_state(magnitude=Fraction(-1, 4))
    with pytest.raises(ValueError):
        _mk_state(magnitude=Fraction(3, 2))


def test_gauge_kind_rejected_when_unknown():
    with pytest.raises(ValueError):
        _mk_state(gauge="volume")


def test_prime_axis_must_be_at_least_two():
    with pytest.raises(ValueError):
        _mk_state(prime_axis=1)


def test_confidence_bounds():
    _mk_state(confidence=None)
    _mk_state(confidence=Fraction(0))
    _mk_state(confidence=Fraction(1))
    with pytest.raises(ValueError):
        _mk_state(confidence=Fraction(-1, 100))
    with pytest.raises(ValueError):
        _mk_state(confidence=Fraction(101, 100))


def test_metric_point_is_alias_for_metric_disk_state():
    assert ucns_g.MetricPoint is ucns_g.MetricDiskState


# ---------------------------------------------------------------------------
# Twist vs phase pin
# ---------------------------------------------------------------------------


def test_same_phase_distinguished_by_twist_ordinal():
    """v3 pin: same phase != same state.

    Two states at phase=0 but different twist ordinals must be
    distinguishable records. This is what prevents global non-closure
    from being confused with local disk closure.
    """
    s0 = _mk_state(twist_ordinal=0, phase=Fraction(0), face=1)
    s1 = _mk_state(twist_ordinal=1, phase=Fraction(0), face=-1)
    s2 = _mk_state(twist_ordinal=2, phase=Fraction(0), face=1)

    assert s0 != s1
    assert s1 != s2
    assert s0 != s2


def test_mobius_face_alternation_holds_across_twist_ordinals():
    """Spec rule: face_{n+1} = -face_n.

    The schema does not enforce alternation across separate constructed
    records (that's the cylinder-trace builder's job), but the schema
    does permit the canonical pattern.
    """
    chain = [
        _mk_state(twist_ordinal=n, phase=Fraction(0), face=(1 if n % 2 == 0 else -1))
        for n in range(4)
    ]
    faces = [s.face for s in chain]
    assert faces == [1, -1, 1, -1]


# ---------------------------------------------------------------------------
# GrainTensor
# ---------------------------------------------------------------------------


def test_grain_tensor_carries_states():
    states = (
        _mk_state(axis="P", prime_axis=2),
        _mk_state(axis="K", prime_axis=3),
        _mk_state(axis="Q", prime_axis=5),
    )
    g = ucns_g.GrainTensor(grain="turn", states=states)
    assert g.grain == "turn"
    assert g.states == states


def test_grain_tensor_rejects_non_state_entries():
    with pytest.raises(TypeError):
        ucns_g.GrainTensor(grain="turn", states=("not-a-state",))  # type: ignore[arg-type]


def test_grain_tensor_rejects_unknown_grain():
    with pytest.raises(ValueError):
        ucns_g.GrainTensor(grain="aeon")  # type: ignore[arg-type]


def test_grain_tensor_default_is_empty_tuple():
    g = ucns_g.GrainTensor(grain="session")
    assert g.states == ()


# ---------------------------------------------------------------------------
# Firewall pin (documentation surface)
# ---------------------------------------------------------------------------


def test_ucns_g_does_not_import_ucns_a_factorization_module():
    """UCNS-A / UCNS-G firewall: the v3 schema package must not depend on
    the recursive UCNS-A factorization algebra (``ucns_v04`` etc.).
    """
    pkg = ucns_g
    schema_src = (ROOT / "edcmbone" / "ucns_g" / "schema.py").read_text()
    primes_src = (ROOT / "edcmbone" / "ucns_g" / "primes.py").read_text()
    init_src = (ROOT / "edcmbone" / "ucns_g" / "__init__.py").read_text()

    for src in (schema_src, primes_src, init_src):
        assert "ucns_v04" not in src
        assert "UCNSObject" not in src
        assert "ucns_recursive" not in src

    # Pin module-level surface too.
    assert "MetricDiskState" in pkg.__all__
    assert "PRIME_AXIS_ASSIGNMENT" in pkg.__all__
