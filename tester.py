from auto_responses.lib.models import Message, AutoResponseMethod, AutoResponseType
from regex import search, fullmatch, escape, IGNORECASE
from auto_response import AUTO_RESPONSE as AU
from importlib import import_module
from time import perf_counter
from typing import Callable


def test(message: Message) -> str:
    if message.content == '':
        return 'Auto responses do not respond to empty messages'

    trigger = AU.trigger if AU.data.regex else escape(AU.trigger)

    match AU.method:
        case AutoResponseMethod.exact:
            match = fullmatch(
                pattern=trigger+r'(\.|\?|\!)*',
                string=message.content,
                flags=0 if AU.data.case_sensitive else IGNORECASE
            )
        case AutoResponseMethod.contains:
            match = search(
                pattern=rf'(^|\s){trigger}(\.|\?|\!)*(\s|$)',
                string=message.content,
                flags=0 if AU.data.case_sensitive else IGNORECASE
            )
        case AutoResponseMethod.regex:
            match = search(
                pattern=AU.trigger,
                string=message.content,
                flags=0 if AU.data.case_sensitive else IGNORECASE
            )
        case AutoResponseMethod.mention:
            match = search(
                pattern=rf'<@!?{AU.trigger}>(\s|$)',
                string=message.content,
                flags=0 if AU.data.case_sensitive else IGNORECASE
            )
        case AutoResponseMethod.disabled:
            return 'Auto response is disabled'
        case _:
            return f'Unknown method: {AU.method}'

    if match is None:
        return 'No match'

    if AU.data.nsfw and not message.channel.nsfw:
        return 'Auto response is nsfw and channel is not nsfw'

    if AU.data.user is not None and message.author.id != AU.data.user:
        return 'User does not match'

    if AU.data.guild is not None and message.guild.id != AU.data.guild:
        return 'Guild does not match'

    match AU.type:
        case AutoResponseType.text:
            return f'Successful text response:\n{AU.response}'
        case AutoResponseType.file:
            return 'File responses are not supported'
        case AutoResponseType.script:
            try:
                on_message: Callable = import_module(
                    f'auto_responses.{AU.response}').on_message
            except ImportError:
                return f'Failed to import script {AU.response}'

            try:
                st = perf_counter()
                response = on_message(message)
                et = perf_counter()
            except Exception as e:
                return f'Failed to execute script {AU.response}: {e}'

            if et-st > 5:
                return f'Script execution took longer than 5 seconds: {et-st:.2f}s'

            if response is None:
                return 'No response from script'

            return f'Successful script response (execution time: {(et-st)*1000:.2f}ms)\n{response}'
        case AutoResponseType.deleted:
            return 'Auto response has been deleted'
        case _:
            return f'Unknown type: {AU.type}'
