from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _parse_py(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _literal_assign_value(module: ast.Module, name: str) -> str:
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
    raise AssertionError(f"{name} not found")


def test_version_constant_and_readme_marker_are_aligned_to_v1_0_1() -> None:
    version_ast = _parse_py(ROOT / "version.py")
    assert _literal_assign_value(version_ast, "__version__") == "1.0.1"

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "**edcmbone v1.0.1**" in readme


def test_operator_public_surface_declares_expected_exports() -> None:
    operator_init_ast = _parse_py(ROOT / "edcmbone" / "operator" / "__init__.py")
    exports = _literal_assign_value(operator_init_ast, "__all__")
    assert set(exports) == {
        "tokenize_turn",
        "count_families",
        "count_turn",
        "count_window",
        "aggregate",
        "OperatorVector",
    }
