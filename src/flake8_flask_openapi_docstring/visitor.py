import ast
from typing import List

from apispec.yaml_utils import load_yaml_from_docstring


class FlaskOpenAPIDocStringVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.results: List[ast.FunctionDef] = []

    def _is_route_decorator(self, node: ast.expr) -> bool:
        if not isinstance(node, ast.Call):
            return False

        if isinstance(node.func, ast.Attribute):
            return node.func.attr == "route"

        if isinstance(node.func, ast.Name):
            return node.func.id == "route"

        return False

    def _has_openapi_docstring(self, node: ast.FunctionDef) -> bool:
        docstring = ast.get_docstring(node)

        if docstring is None:
            return False

        api_spec = load_yaml_from_docstring(docstring)

        return api_spec != {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        has_route_decorators = any(
            self._is_route_decorator(decorator) for decorator in node.decorator_list
        )

        if has_route_decorators:
            has_openapi_docstring = self._has_openapi_docstring(node)

            if not has_openapi_docstring:
                self.results.append(node)
