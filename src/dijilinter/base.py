import ast
import os
from typing import NamedTuple


class Violation(NamedTuple):
    """
    Every rule violation contains a node that breaks the rule,
    and a message that will be shown to the user.
    """

    node: ast.AST
    message: str


class Checker(ast.NodeVisitor):
    """
    A Checker is a Visitor that defines a lint rule, and stores all the
    nodes that violate that lint rule.
    """

    def __init__(self, issue_code):
        self.issue_code = issue_code
        self.violations = set()


class Linter:
    """Holds all list rules, and runs them against a source file."""

    def __init__(self):
        self.checkers = set()

    @staticmethod
    def print_violations(checker, file_name):
        for node, message in checker.violations:
            print(
                f"{file_name}:{node.lineno}:{node.col_offset}: "
                f"{checker.issue_code}: {message}"
            )

    def run(self, source_path):
        """Runs all lints on a source file."""
        file_name = os.path.basename(source_path)

        with open(source_path) as source_file:
            source_code = source_file.read()

        tree = ast.parse(source_code)
        for checker in self.checkers:
            checker.visit(tree)
            self.print_violations(checker, file_name)
