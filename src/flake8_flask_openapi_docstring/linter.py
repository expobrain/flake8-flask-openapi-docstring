from __future__ import annotations

import ast
from typing import Iterable, Tuple, Type

from flake8_flask_openapi_docstring.__version__ import __version__
from flake8_flask_openapi_docstring.visitor import FlaskOpenAPIDocStringVisitor

LintErrorResult = Tuple[int, int, str, Type["FlaskOpenAPIDocStringLinter"]]


class FlaskOpenAPIDocStringLinter:
    name = "flake8_openapi_docstring"
    version = __version__

    def __init__(self, tree: ast.Module) -> None:
        self.tree = tree

    @classmethod
    def error(cls, lineno: int, offset: int, code: str, message: str) -> LintErrorResult:
        return (lineno, offset, f"{code} {message}", cls)

    def run(self) -> Iterable[LintErrorResult]:
        visitor = FlaskOpenAPIDocStringVisitor()
        visitor.visit(self.tree)

        for node in visitor.results:
            yield self.error(
                node.lineno, node.col_offset, "FO100", "Missing OpenAPI fragment in docstring"
            )
