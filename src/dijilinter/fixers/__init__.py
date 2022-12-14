from __future__ import annotations

from typing import TYPE_CHECKING, Set, Type

from .base import BaseFixer

if TYPE_CHECKING:
    from dijilinter.filters import GlobalSettings

FIXER_CLASSES: Set[Type[BaseFixer]] = {}


def get_fixers_chain(global_settings: GlobalSettings) -> Set[BaseFixer]:
    fixers = {
        fixercls()
        for fixercls in FIXER_CLASSES
        if global_settings.should_run_processor(fixercls)
    }
    return fixers
