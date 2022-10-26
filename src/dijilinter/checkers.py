import ast

from .base import Checker, Violation


class ModelPermissionChecker(Checker):
    def visit_ClassDef(self, node):
        if not any(
            isinstance(x, ast.Attribute)
            and x.value.id == "models"
            and x.attr == "Model"
            for x in node.bases
        ):
            return

        has_default = False

        for element in node.body:
            if (
                isinstance(element, ast.Assign)
                and any(x.id == "default_permissions" for x in element.targets)
                and isinstance(element.value, ast.Call)
                and element.value.func.id == "Permission"
            ):
                has_default = True
                break

        if not has_default:
            self.violations.add(
                Violation(
                    node,
                    message=f"{node.name} model does not have default_pesmission variable.",
                )
            )
