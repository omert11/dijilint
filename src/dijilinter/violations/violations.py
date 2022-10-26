from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any, Tuple


@dataclass
class Violation:
    code: str
    line: int
    col: int
    description: str
    filename: str
    node: ast.AST

    @classmethod
    def build(
        cls,
        filename: str,
        vio_details: Tuple[str, str],
        node: ast.AST,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> Violation:
        code, msg = vio_details
        return cls(code, node.lineno, node.col_offset, msg, filename, node)
