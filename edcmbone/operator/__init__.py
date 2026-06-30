# ratios: loc_comments=11:18 imports_exports=3:1 calls_definitions=0:0
# === MODULE_BUILD ===
# id: operator_public_surface
#   module_name: operator package exports
#   module_kind: service
#   summary: defines stable public exports for operator tokenization, counting, and aggregation.
#   owner: edcmbone-maintainers
#   public_surface: tokenize_turn,count_families,count_turn,count_window,aggregate,OperatorVector
#   internal_surface: __all__
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: read
#   admin_only: false
#   tests: tests/test_smoke.py,tests/test_backend.py
#   rollout: default_enabled
#   rollback: remove exports from __all__ and package init
#   unresolved: hmmm mandatory boundary object that records unresolved constraint, preserves honest incompletion, and marks the transition between delivered output and living continuation
# === END MODULE_BUILD ===
from .tokenize import tokenize_turn
from .count import count_families, count_turn, count_window
from .aggregate import aggregate, OperatorVector

__all__ = [
    "tokenize_turn",
    "count_families",
    "count_turn",
    "count_window",
    "aggregate",
    "OperatorVector",
]
# ratios: loc_comments=11:18 imports_exports=3:1 calls_definitions=0:0
