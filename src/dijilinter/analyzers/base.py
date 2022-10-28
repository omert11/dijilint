import ast
from abc import ABC
from typing import Any, List, Type

from dijilinter.processors import Processor
from dijilinter.violations import Violation


class BaseAnalyzer(ABC, Processor, ast.NodeVisitor):
    violation_type: Type[Violation] = Violation

    def __init__(self):
        self.violations: List[Violation] = []

    def _mark_violation(self, *nodes: ast.AST, **kwargs: Any) -> None:  # noqa: ANN401
        klass = self.violation_type
        for node in nodes:
            violation = klass.build(self.filename, self.violation_code, node, **kwargs)
            self.violations.append(violation)

    def check(self, tree: ast.AST, filename: str) -> List[Violation]:
        self.filename = filename
        self.violations = []

        self.visit(tree)

        return self.violations
