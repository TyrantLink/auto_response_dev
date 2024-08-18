from importlib import import_module
from dataclasses import dataclass
from typing import Callable
from .aulib import (
    ScriptAuthor,
    Response,
    Message,
    Channel,
    Guild,
    User
)


@dataclass
class ScriptedAutoResponse:
    function: Callable[[Message], Response | None]
    author: ScriptAuthor


class ScriptedAutoResponseManager:
    def __init__(self) -> None:
        self.cache: dict[str, Callable] = {}

    def get(self, script: str) -> ScriptedAutoResponse:
        if script in self.cache:
            return self.cache[script]

        module = import_module(
            f'{__name__}.auto_responses.{script}'
        )

        self.cache[script] = ScriptedAutoResponse(
            function=module.on_message,
            author=module.author
        )
        return self.cache[script]


SCRIPTED_AUTO_RESPONSES = ScriptedAutoResponseManager()
