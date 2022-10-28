import ast
from typing import Union

from dijilinter.violations import VerboseReraiseViolation, codes

from .base import BaseAnalyzer


class ModelPermissionAnalyzer(BaseAnalyzer):
    violation_code = codes.FORGOT_DEFAULTPERMISSION
    violation_type = VerboseReraiseViolation

    def _is_sub_models_Model(self, node: Union[ast.stmt, ast.expr]) -> bool:
        return any(
            isinstance(x, ast.Attribute)
            and x.value.id == "models"
            and x.attr == "Model"
            for x in node.bases
        )

    def _has_permission(self, element):
        return (
            isinstance(element, ast.Assign)
            and any(x.id == "default_permissions" for x in element.targets)
            and isinstance(element.value, ast.Call)
            and element.value.func.id == "Permission"
        )

    def _has_default_permission(self, node: Union[ast.stmt, ast.expr]) -> bool:
        for element in node.body:
            if self._has_permission(element):
                return True
        return False

    def visit_ClassDef(self, node):
        if not self._is_sub_models_Model(node):
            return

        if not self._has_default_permission(node):
            self._mark_violation(node)
            # f"{node.name} model does not have default_pesmission variable.",
