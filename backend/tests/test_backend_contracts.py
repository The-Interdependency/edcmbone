from pathlib import Path
import ast

import edcmbone_backend as backend
import ucns


def test_backend_imports_only_ucns():
    source = Path(backend.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")
    assert set(imports) == {"ucns"}
    assert imports == ["ucns"]


def test_hmmm_preserves_unresolved_constraint():
    boundary = backend.make_boundary(
        "delivered output",
        "The external The-Interdependency/skill-lib path remains unresolved.",
    )

    assert boundary.delivered == "delivered output"
    assert isinstance(boundary.hmmm, backend.Hmmm)
    assert "The-Interdependency/skill-lib" in str(boundary.hmmm)
    assert backend.serialize_boundary(boundary)["hmmm"]["text"] == str(boundary.hmmm)


def test_hmmm_fallback_is_never_empty():
    boundary = backend.make_boundary("delivered output")

    assert isinstance(boundary.hmmm, backend.Hmmm)
    assert boundary.hmmm.transition == "hmmm"
    assert str(boundary.hmmm).startswith("hmmm:")
    assert backend.serialize_boundary(boundary)["hmmm"]["text"] == str(boundary.hmmm)


def test_boundary_objects_are_ucns_backed():
    left = backend.make_boundary("left", "left unresolved")
    right = backend.make_boundary("right")
    merged = backend.merge_boundaries(left, right)
    expected = ucns.multiply(left.ucns_object, right.ucns_object)

    assert isinstance(left.ucns_object, ucns.UCNSObject)
    assert isinstance(merged.ucns_object, ucns.UCNSObject)
    assert merged.ucns_object.equivalent(expected)
    assert merged.delivered == "left\nright"
    assert isinstance(merged.hmmm, backend.Hmmm)
    assert "left unresolved" in str(merged.hmmm)


def _source_text():
    return Path(backend.__file__).read_text(encoding="utf-8")


def test_canonical_skill_lib_blocks_are_declared():
    source = _source_text()

    for block in ("MODULE_BUILD", "CONTRACTS", "DEPENDENCIES", "BOUNDARIES", "DOCS"):
        assert f"# === {block} ===" in source
        assert f"# === END {block} ===" in source
    assert "canonical https://github.com/The-Interdependency/skill-lib guidance verified" in source
    assert "The requested The-Interdependency/skill-lib path was not present" not in source


def test_boundaries_record_no_hidden_side_effects():
    source = _source_text()

    assert "#   auth_boundary: none" in source
    assert "#   storage_boundary: none" in source
    assert "#   network_boundary: none" in source
    assert "#   admin_only: false" in source


def test_backend_src_path_is_self_contained(tmp_path):
    import os
    import subprocess
    import sys

    code = """
import edcmbone_backend as backend
boundary = backend.make_boundary('delivered', 'unresolved')
assert boundary.ucns_object.n_min == 1
assert backend.serialize_boundary(boundary)['hmmm']['text'] == 'unresolved'
"""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    result = subprocess.run(
        [sys.executable, "-c", code],
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
