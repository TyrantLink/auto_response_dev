from typing import Callable
from .dad_bot import on_message as dad_bot
from .april_fools_rat import on_message as april_fools_rat


SCRIPTED_AUTO_RESPONSES: dict[str, Callable] = {
    's1': dad_bot,
    's2': april_fools_rat,
}
