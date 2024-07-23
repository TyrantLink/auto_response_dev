from importlib import import_module
from typing import Callable


class ScriptedAutoResponseManager:
    def __init__(self) -> None:
        self.cache: dict[str, Callable] = {}

    def get(self, script: str) -> Callable:
        if script in self.cache:
            return self.cache[script]

        self.cache[script] = import_module(f'{__name__}.{script}').on_message
        return self.cache[script]


SCRIPTED_AUTO_RESPONSES = ScriptedAutoResponseManager()
