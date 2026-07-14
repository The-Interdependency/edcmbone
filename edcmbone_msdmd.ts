import { defineMsdmdCollection } from "./.agents/skills/msdmd/collection";

export default defineMsdmdCollection({
  "declarations": [
    {
      "block": "BOUNDARIES",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "network_boundary": "none",
        "owner": "The Interdependency",
        "pii": "possible",
        "secrets": "none",
        "side_effects": "none",
        "since": "2026-06-25",
        "storage_boundary": "none",
        "summary": "in-memory UCNS boundary-object construction from caller-supplied text; no auth, persistence, network, admin action, secrets, or PII handling beyond caller-provided content",
        "user_data_boundary": "none"
      },
      "file": "backend/src/edcmbone_backend/__init__.py",
      "id": "edcmbone_backend_runtime_boundary"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "tests.test_backend_contracts.test_backend_imports_only_ucns",
        "class": "architecture",
        "given": "the new backend package source is inspected",
        "then": "its only import statement imports ucns"
      },
      "file": "backend/src/edcmbone_backend/__init__.py",
      "id": "backend_imports_only_ucns"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "tests.test_backend_contracts.test_boundary_objects_are_ucns_backed",
        "class": "correctness",
        "given": "a boundary is created or merged",
        "then": "each boundary carries a normalized UCNS object and merged boundaries multiply their UCNS carriers"
      },
      "file": "backend/src/edcmbone_backend/__init__.py",
      "id": "boundary_objects_are_ucns_backed"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "tests.test_backend_contracts.test_hmmm_fallback_is_never_empty",
        "class": "correctness",
        "given": "a boundary is created without an explicit unresolved constraint",
        "then": "hmmm still records an honest continuation marker"
      },
      "file": "backend/src/edcmbone_backend/__init__.py",
      "id": "hmmm_fallback_is_never_empty"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "call": "tests.test_backend_contracts.test_hmmm_preserves_unresolved_constraint",
        "class": "correctness",
        "given": "a boundary is created with delivered output and an unresolved constraint",
        "then": "hmmm is an object and keeps the unresolved text intact"
      },
      "file": "backend/src/edcmbone_backend/__init__.py",
      "id": "hmmm_preserves_unresolved_constraint"
    },
    {
      "block": "DEPENDENCIES",
      "fields": {
        "calls": "ucns.UCNSObject,ucns.AnchorPayload,ucns.multiply",
        "class": "runtime",
        "direction": "outbound",
        "imports": "ucns",
        "owner": "The Interdependency",
        "provides": "BoundaryObject,Hmmm,make_boundary,merge_boundaries,serialize_boundary",
        "since": "2026-06-25",
        "summary": "backend imports only ucns and calls UCNSObject construction, AnchorPayload construction, normalization, and multiply for carrier composition"
      },
      "file": "backend/src/edcmbone_backend/__init__.py",
      "id": "edcmbone_backend_dependency_edges"
    },
    {
      "block": "DOCS",
      "fields": {
        "audience": "developer",
        "covers": "BoundaryObject,Hmmm,make_boundary,merge_boundaries,serialize_boundary",
        "owner": "The Interdependency",
        "since": "2026-06-25",
        "source": "backend/README.md#usage-guidance",
        "status": "current",
        "summary": "README usage guidance for creating, merging, and serializing UCNS-backed boundary objects"
      },
      "file": "backend/src/edcmbone_backend/__init__.py",
      "id": "edcmbone_backend_usage_docs"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_coerce_text,_anchor",
        "module_kind": "backend",
        "module_name": "edcmbone_backend",
        "network_boundary": "none",
        "owner": "The Interdependency",
        "public_surface": "BoundaryObject,Hmmm,make_boundary,merge_boundaries,serialize_boundary,hmmm",
        "requires": "ucns",
        "rollback": "restore backend_old as backend",
        "rollout": "default_enabled",
        "since": "2026-06-25",
        "storage_boundary": "none",
        "summary": "UCNS-only backend that records delivered output and unresolved constraints as explicit hmmm boundary objects",
        "tests": "tests.test_backend_contracts",
        "unresolved": "none; canonical https://github.com/The-Interdependency/skill-lib guidance verified on 2026-06-25",
        "user_data_boundary": "caller supplied text only; no persistence"
      },
      "file": "backend/src/edcmbone_backend/__init__.py",
      "id": "edcmbone_backend_ucns_boundary"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_load",
        "module_kind": "adapter",
        "module_name": "loader",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "CanonLoader",
        "requires": "none",
        "rollback": "remove module; parser falls back to no embedded canon",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "read",
        "summary": "loads the v1 canon data files (bones/affixes/punct/markers) and exposes a lookup API",
        "tests": "hmmm",
        "unresolved": "dedicated canon-loader test module not located in tracked tests/",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/canon/loader.py",
      "id": "edcmbone_canon_loader"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_tok_to_dict,_dict_to_tok,_metrics_to_dict,_dict_to_metrics,_build_huffman_codes,_huffman_expected_bits",
        "module_kind": "engine",
        "module_name": "compress",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "encode,decode,to_bytes,from_bytes,compression_stats",
        "requires": "edcmbone_parser_turns_rounds,edcmbone_metrics_compute",
        "rollback": "remove module; transcripts persist uncompressed",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "lossless EDCM-aware codec for ParsedTranscript + RoundMetrics (separate bone/flesh streams, zlib entropy coding)",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/compress.py",
      "id": "edcmbone_compress"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_compute_R,_compute_F,_compute_L,_compute_N,_compute_P,_compute_O,_compute_I,_compute_C,_compute_D,_compute_E,_build_phrase_patterns,_count_marker_hits",
        "module_kind": "engine",
        "module_name": "compute",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "RoundMetrics,compute_round,compute_transcript,energy_step",
        "requires": "edcmbone_metrics_stats,edcmbone_metrics_risk,edcmbone_canon_loader",
        "rollback": "remove module; no behavioral metric vector produced",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "computes the EDCM metric vector M_t and dissonance energy for a parsed round/transcript",
        "tests": "tests.test_metrics_layer_designation",
        "unresolved": "per its own docstring this layer-A module canonically belongs upstream in the future edcm package",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/metrics/compute.py",
      "id": "edcmbone_metrics_compute"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "matrix",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "freeze, diff",
        "requires": "none",
        "rollback": "remove module; metric projection loses its frozen coefficient source",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "explicit freezable A matrix (Layer0->Layer1) and PROJECTION_MAP (Layer1->Layer3) as versioned, diffable dicts",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/metrics/matrix.py",
      "id": "edcmbone_metrics_matrix"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_clamp_unit, _sign",
        "module_kind": "engine",
        "module_name": "orthogonality",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "AxisState, MetricAxis, MetricReadout, ConstraintField, FieldMotion, field_motion_fixture, canonical_axes",
        "requires": "none",
        "rollback": "remove module; v0.2 signed-axis metric construction unavailable",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "v0.2 signed-axis metric-identity model and the UCNS construction objects (ConstraintField/FieldMotion) the EDCM metric spec is built around",
        "tests": "tests.test_metric_orthogonality_v02",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/metrics/orthogonality.py",
      "id": "edcmbone_metrics_orthogonality"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "projection",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "AgentMetrics, project, project_transcript, gini_tbf, fire_alerts, crosswalk_risk",
        "requires": "edcmbone_metrics_matrix",
        "rollback": "remove module; agent-facing 6-metric view unavailable",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "projects the 11 Layer-1 Arc-Style metrics to the 6 agent-facing metrics (CM, DA, DRIFT, DVG, INT, TBF)",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/metrics/projection.py",
      "id": "edcmbone_metrics_projection"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "risk",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "fixation_risk, broken_return, escalation_risk, stagnation_risk, loop_risk",
        "requires": "none",
        "rollback": "remove module; risk composites unavailable",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "the EDCM risk proxies (fixation, broken-return, escalation, stagnation, loop), all clamped to [0,1]",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/metrics/risk.py",
      "id": "edcmbone_metrics_risk"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_count_vector",
        "module_kind": "engine",
        "module_name": "stats",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "tokenize, ngrams, ttr, repetition_ratio, shannon_entropy, rep_ngram_density, pattern_density, novelty, cosine_sim, jaccard, correction_fidelity, clamp, norm_per_100",
        "requires": "none",
        "rollback": "remove module; metric primitives unavailable",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "stdlib-only text statistics (TTR, entropy, novelty, cosine, n-gram density) feeding the EDCM metric vector",
        "tests": "hmmm",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/metrics/stats.py",
      "id": "edcmbone_metrics_stats"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_BoneClassifier, _split_turns, _group_into_rounds, _raw_tokens, _ordered_unique",
        "module_kind": "engine",
        "module_name": "turns_rounds",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "parse_transcript, BoneToken, FleshToken, Turn, Round, ParsedTranscript",
        "requires": "edcmbone_canon_loader",
        "rollback": "remove module; transcripts cannot be parsed into the EDCM structure",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "embedded rule-based transcript parser (canon-driven, no ML deps) producing bones/flesh tokens, turns, and rounds",
        "tests": "tests.test_apostrophe_normalization_and_tokenization",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/parser/turns_rounds.py",
      "id": "edcmbone_parser_turns_rounds"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_class_anchor, _wrap_with_class, _feature_payload, _build_dispatch_table",
        "module_kind": "adapter",
        "module_name": "closed_tokens",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "encode, class_of, feature_payload_of",
        "requires": "edcmbone_ucns_v04",
        "rollback": "remove module; closed-token UCNS encoding unavailable",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "encodes English closed-class tokens, whitespace, punctuation, and small numerals to UCNS objects on a 16-gon host carrier",
        "tests": "tests.test_closed_tokens",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/ucns/closed_tokens.py",
      "id": "edcmbone_ucns_closed_tokens"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_lcm, _reduce_lcm",
        "module_kind": "engine",
        "module_name": "ucns_v04",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "AnchorPayload, UCNSObject, unit_obj, is_unit_payload, multiply",
        "requires": "none",
        "rollback": "remove module; closed_tokens loses its UCNS object algebra",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "local UCNS engine using the turn-fraction angle convention on the doubled cover of the unit circle",
        "tests": "tests.test_ucns_objects",
        "unresolved": "this is edcmbone's local UCNS-A layer; per docs/ucns-boundary.md no UCNS-A theorem status transfers to EDCM/UCNS-G",
        "user_data_boundary": "none"
      },
      "file": "backend_old/src/edcmbone/ucns/ucns_v04.py",
      "id": "edcmbone_ucns_v04"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "__all__",
        "module_kind": "service",
        "module_name": "operator package exports",
        "network_boundary": "none",
        "owner": "edcmbone-maintainers",
        "public_surface": "tokenize_turn,count_families,count_turn,count_window,aggregate,OperatorVector",
        "rollback": "remove exports from __all__ and package init",
        "rollout": "default_enabled",
        "storage_boundary": "none",
        "summary": "defines stable public exports for operator tokenization, counting, and aggregation.",
        "tests": "tests/test_smoke.py,tests/test_backend.py",
        "unresolved": "hmmm mandatory boundary object that records unresolved constraint, preserves honest incompletion, and marks the transition between delivered output and living continuation",
        "user_data_boundary": "read"
      },
      "file": "edcmbone/edcmbone/operator/__init__.py",
      "id": "operator_public_surface"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "FAMILIES",
        "module_kind": "engine",
        "module_name": "operator aggregate",
        "network_boundary": "none",
        "owner": "edcmbone-maintainers",
        "public_surface": "aggregate,OperatorVector",
        "rollback": "route callers back to raw counts",
        "rollout": "default_enabled",
        "storage_boundary": "none",
        "summary": "normalizes operator family counts into a stable 5D unit-sum vector.",
        "tests": "tests/test_backend.py",
        "user_data_boundary": "read"
      },
      "file": "edcmbone/edcmbone/operator/aggregate.py",
      "id": "operator_vector_aggregate"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "FAMILIES",
        "module_kind": "service",
        "module_name": "operator family count",
        "network_boundary": "none",
        "owner": "edcmbone-maintainers",
        "public_surface": "count_families,count_turn,count_window",
        "rollback": "remove public counter entrypoints and call sites",
        "rollout": "default_enabled",
        "storage_boundary": "none",
        "summary": "counts P/K/Q/T/S family assignments per turn and across windows.",
        "tests": "tests/test_backend.py",
        "user_data_boundary": "read"
      },
      "file": "edcmbone/edcmbone/operator/count.py",
      "id": "operator_family_count"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_family,_normalize_apos,_WORD_FAMILY,_FRAG_FAMILY,_STANDALONE_PUNCT",
        "module_kind": "engine",
        "module_name": "operator tokenizer",
        "network_boundary": "none",
        "owner": "edcmbone-maintainers",
        "public_surface": "tokenize_turn",
        "rollback": "swap callers to legacy tokenizer and remove export",
        "rollout": "default_enabled",
        "storage_boundary": "none",
        "summary": "tokenizes turns and maps closed-class tokens into operator families with canon-priority rules.",
        "tests": "hmmm",
        "user_data_boundary": "read"
      },
      "file": "edcmbone/edcmbone/operator/tokenize.py",
      "id": "operator_tokenization"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "__all__",
        "module_kind": "service",
        "module_name": "operator package exports",
        "network_boundary": "none",
        "owner": "edcmbone-maintainers",
        "public_surface": "tokenize_turn,count_families,count_turn,count_window,aggregate,OperatorVector",
        "rollback": "remove exports from __all__ and package init",
        "rollout": "default_enabled",
        "storage_boundary": "none",
        "summary": "defines stable public exports for operator tokenization, counting, and aggregation.",
        "tests": "tests/test_smoke.py,tests/test_backend.py",
        "unresolved": "hmmm mandatory boundary object that records unresolved constraint, preserves honest incompletion, and marks the transition between delivered output and living continuation",
        "user_data_boundary": "read"
      },
      "file": "edcmbone/operator/__init__.py",
      "id": "operator_public_surface"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "FAMILIES",
        "module_kind": "engine",
        "module_name": "operator aggregate",
        "network_boundary": "none",
        "owner": "edcmbone-maintainers",
        "public_surface": "aggregate,OperatorVector",
        "rollback": "route callers back to raw counts",
        "rollout": "default_enabled",
        "storage_boundary": "none",
        "summary": "normalizes operator family counts into a stable 5D unit-sum vector.",
        "tests": "tests/test_backend.py",
        "user_data_boundary": "read"
      },
      "file": "edcmbone/operator/aggregate.py",
      "id": "operator_vector_aggregate"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "FAMILIES",
        "module_kind": "service",
        "module_name": "operator family count",
        "network_boundary": "none",
        "owner": "edcmbone-maintainers",
        "public_surface": "count_families,count_turn,count_window",
        "rollback": "remove public counter entrypoints and call sites",
        "rollout": "default_enabled",
        "storage_boundary": "none",
        "summary": "counts P/K/Q/T/S family assignments per turn and across windows.",
        "tests": "tests/test_backend.py",
        "user_data_boundary": "read"
      },
      "file": "edcmbone/operator/count.py",
      "id": "operator_family_count"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_family,_normalize_apos,_WORD_FAMILY,_FRAG_FAMILY,_STANDALONE_PUNCT",
        "module_kind": "engine",
        "module_name": "operator tokenizer",
        "network_boundary": "none",
        "owner": "edcmbone-maintainers",
        "public_surface": "tokenize_turn",
        "rollback": "swap callers to legacy tokenizer and remove export",
        "rollout": "default_enabled",
        "storage_boundary": "none",
        "summary": "tokenizes turns and maps closed-class tokens into operator families with canon-priority rules.",
        "tests": "tests/test_apostrophe_normalization_and_tokenization.py,tests/test_backend.py",
        "user_data_boundary": "read"
      },
      "file": "edcmbone/operator/tokenize.py",
      "id": "operator_tokenization"
    }
  ],
  "edges": [
    {
      "from": "edcmbone_backend_runtime_boundary",
      "kind": "owns",
      "source_block": "BOUNDARIES",
      "source_id": "edcmbone_backend_runtime_boundary",
      "to": "The Interdependency"
    },
    {
      "from": "backend_imports_only_ucns",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "backend_imports_only_ucns",
      "to": "tests.test_backend_contracts.test_backend_imports_only_ucns"
    },
    {
      "from": "boundary_objects_are_ucns_backed",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "boundary_objects_are_ucns_backed",
      "to": "tests.test_backend_contracts.test_boundary_objects_are_ucns_backed"
    },
    {
      "from": "hmmm_fallback_is_never_empty",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "hmmm_fallback_is_never_empty",
      "to": "tests.test_backend_contracts.test_hmmm_fallback_is_never_empty"
    },
    {
      "from": "hmmm_preserves_unresolved_constraint",
      "kind": "calls",
      "source_block": "CONTRACTS",
      "source_id": "hmmm_preserves_unresolved_constraint",
      "to": "tests.test_backend_contracts.test_hmmm_preserves_unresolved_constraint"
    },
    {
      "from": "edcmbone_backend_dependency_edges",
      "kind": "owns",
      "source_block": "DEPENDENCIES",
      "source_id": "edcmbone_backend_dependency_edges",
      "to": "The Interdependency"
    },
    {
      "from": "edcmbone_backend_usage_docs",
      "kind": "covers",
      "source_block": "DOCS",
      "source_id": "edcmbone_backend_usage_docs",
      "to": "BoundaryObject"
    },
    {
      "from": "edcmbone_backend_usage_docs",
      "kind": "covers",
      "source_block": "DOCS",
      "source_id": "edcmbone_backend_usage_docs",
      "to": "Hmmm"
    },
    {
      "from": "edcmbone_backend_usage_docs",
      "kind": "covers",
      "source_block": "DOCS",
      "source_id": "edcmbone_backend_usage_docs",
      "to": "make_boundary"
    },
    {
      "from": "edcmbone_backend_usage_docs",
      "kind": "covers",
      "source_block": "DOCS",
      "source_id": "edcmbone_backend_usage_docs",
      "to": "merge_boundaries"
    },
    {
      "from": "edcmbone_backend_usage_docs",
      "kind": "covers",
      "source_block": "DOCS",
      "source_id": "edcmbone_backend_usage_docs",
      "to": "serialize_boundary"
    },
    {
      "from": "edcmbone_backend_usage_docs",
      "kind": "owns",
      "source_block": "DOCS",
      "source_id": "edcmbone_backend_usage_docs",
      "to": "The Interdependency"
    },
    {
      "from": "edcmbone_backend_ucns_boundary",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_backend_ucns_boundary",
      "to": "The Interdependency"
    },
    {
      "from": "edcmbone_backend_ucns_boundary",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_backend_ucns_boundary",
      "to": "ucns"
    },
    {
      "from": "edcmbone_canon_loader",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_canon_loader",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_canon_loader",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_canon_loader",
      "to": "none"
    },
    {
      "from": "edcmbone_compress",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_compress",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_compress",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_compress",
      "to": "edcmbone_metrics_compute"
    },
    {
      "from": "edcmbone_compress",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_compress",
      "to": "edcmbone_parser_turns_rounds"
    },
    {
      "from": "edcmbone_metrics_compute",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_compute",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_compute",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_compute",
      "to": "edcmbone_canon_loader"
    },
    {
      "from": "edcmbone_metrics_compute",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_compute",
      "to": "edcmbone_metrics_risk"
    },
    {
      "from": "edcmbone_metrics_compute",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_compute",
      "to": "edcmbone_metrics_stats"
    },
    {
      "from": "edcmbone_metrics_matrix",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_matrix",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_matrix",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_matrix",
      "to": "none"
    },
    {
      "from": "edcmbone_metrics_orthogonality",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_orthogonality",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_orthogonality",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_orthogonality",
      "to": "none"
    },
    {
      "from": "edcmbone_metrics_projection",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_projection",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_projection",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_projection",
      "to": "edcmbone_metrics_matrix"
    },
    {
      "from": "edcmbone_metrics_risk",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_risk",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_risk",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_risk",
      "to": "none"
    },
    {
      "from": "edcmbone_metrics_stats",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_stats",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_metrics_stats",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_metrics_stats",
      "to": "none"
    },
    {
      "from": "edcmbone_parser_turns_rounds",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_parser_turns_rounds",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_parser_turns_rounds",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_parser_turns_rounds",
      "to": "edcmbone_canon_loader"
    },
    {
      "from": "edcmbone_ucns_closed_tokens",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_ucns_closed_tokens",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_ucns_closed_tokens",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_ucns_closed_tokens",
      "to": "edcmbone_ucns_v04"
    },
    {
      "from": "edcmbone_ucns_v04",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_ucns_v04",
      "to": "Erin Spencer"
    },
    {
      "from": "edcmbone_ucns_v04",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "edcmbone_ucns_v04",
      "to": "none"
    },
    {
      "from": "operator_family_count",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "operator_family_count",
      "to": "edcmbone-maintainers"
    },
    {
      "from": "operator_family_count",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "operator_family_count",
      "to": "edcmbone-maintainers"
    },
    {
      "from": "operator_public_surface",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "operator_public_surface",
      "to": "edcmbone-maintainers"
    },
    {
      "from": "operator_public_surface",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "operator_public_surface",
      "to": "edcmbone-maintainers"
    },
    {
      "from": "operator_tokenization",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "operator_tokenization",
      "to": "edcmbone-maintainers"
    },
    {
      "from": "operator_tokenization",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "operator_tokenization",
      "to": "edcmbone-maintainers"
    },
    {
      "from": "operator_vector_aggregate",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "operator_vector_aggregate",
      "to": "edcmbone-maintainers"
    },
    {
      "from": "operator_vector_aggregate",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "operator_vector_aggregate",
      "to": "edcmbone-maintainers"
    }
  ],
  "gaps": [],
  "repo": "edcmbone",
  "source_commit": "ebb1e88"
});
