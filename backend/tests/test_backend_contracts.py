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
    assert imports == ["ucns"]


def test_hmmm_preserves_unresolved_constraint():
    boundary = backend.make_boundary(
        "delivered output",
        "The external The-Interdependency/skill-lib path remains unresolved.",
    )

    assert boundary.delivered == "delivered output"
    assert "The-Interdependency/skill-lib" in boundary.hmmm
    assert backend.serialize_boundary(boundary)["hmmm"] == boundary.hmmm


def test_boundary_objects_are_ucns_backed():
    left = backend.make_boundary("left", "left unresolved")
    right = backend.make_boundary("right")
    merged = backend.merge_boundaries(left, right)
    expected = ucns.multiply(left.ucns_object, right.ucns_object)

    assert isinstance(left.ucns_object, ucns.UCNSObject)
    assert isinstance(merged.ucns_object, ucns.UCNSObject)
    assert merged.ucns_object.equivalent(expected)
    assert merged.delivered == "left\nright"
    assert "left unresolved" in merged.hmmm
