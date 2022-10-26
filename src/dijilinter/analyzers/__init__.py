from __future__ import annotations

from typing import TYPE_CHECKING, Set, Type, cast

from . import model
from .base import BaseAnalyzer

if TYPE_CHECKING:
    from dijilinter.filters import GlobalSettings


ANALYZER_CLASSES: Set[Type[BaseAnalyzer]] = {
    model.ModelPermissionAnalyzer,
}


def get_analyzer_chain(global_settings: GlobalSettings) -> Set[BaseAnalyzer]:
    analyzers = {
        analyzercls()
        for analyzercls in ANALYZER_CLASSES
        if global_settings.should_run_processor(analyzercls)
    }
    return analyzers
