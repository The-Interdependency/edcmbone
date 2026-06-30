# ratios: loc_comments=40:14 imports_exports=2:1 calls_definitions=0:0
"""
edcmbone.ucns_g
~~~~~~~~~~~~~~~

UCNS-G v3 metric-geometry schema package.

Pins UCNS-G as a prime-indexed tensor of non-closing Möbius-cylinder metric
disks. See ``docs/handoffs/2026-05-22-ucns-g-prime-cylinder-v3.md`` for the
canonical specification.

This package is intentionally schema-only. It does not replace the scalar
EDCM metric vector in ``Backend/src/edcmbone/metrics/compute.py`` /
``backend/src/edcmbone/metrics/compute.py``; scalar values continue to live
there as the local-projection / magnitude readout.

UCNS-A / UCNS-G firewall: nothing in this package inherits proof status from
UCNS-A.
"""

from .schema import (
    AxisSign,
    AxisState,
    Face,
    GaugeKind,
    Grain,
    MetricAxis,
    MetricDiskState,
    MetricPoint,
    GrainTensor,
    UnitGauge,
    make_metric_disk_state,
    mobius_face_for_twist,
    split_ordinal_phase,
)
from .primes import (
    PRIME_AXIS_ASSIGNMENT,
    PRIMITIVE_OPERATOR_AXES,
    PRIMITIVE_METRIC_AXES,
    prime_for_axis,
)

__all__ = [
    "AxisSign",
    "AxisState",
    "Face",
    "GaugeKind",
    "Grain",
    "MetricAxis",
    "MetricDiskState",
    "MetricPoint",
    "GrainTensor",
    "UnitGauge",
    "make_metric_disk_state",
    "mobius_face_for_twist",
    "split_ordinal_phase",
    "PRIME_AXIS_ASSIGNMENT",
    "PRIMITIVE_OPERATOR_AXES",
    "PRIMITIVE_METRIC_AXES",
    "prime_for_axis",
]
# ratios: loc_comments=40:14 imports_exports=2:1 calls_definitions=0:0
