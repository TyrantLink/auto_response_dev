from aulib import Response, Message, AutoResponseMethod, AutoResponseType, AutoResponse
from regex import search, fullmatch, escape, IGNORECASE
from importlib import import_module
from time import perf_counter
from typing import Callable


def test_au(message: Message, au: AutoResponse) -> str:
    if message.content == '':
        return 'Auto responses do not respond to empty messages'

    trigger = au.trigger if au.data.regex else escape(au.trigger)

    match au.method:
        case AutoResponseMethod.exact:
            match = fullmatch(
                pattern=trigger+r'(\.|\?|\!)*',
                string=message.content,
                flags=0 if au.data.case_sensitive else IGNORECASE
            )
        case AutoResponseMethod.contains:
            match = search(
                pattern=rf'(^|\s){trigger}(\.|\?|\!)*(\s|$)',
                string=message.content,
                flags=0 if au.data.case_sensitive else IGNORECASE
            )
        case AutoResponseMethod.regex:
            match = search(
                pattern=au.trigger,
                string=message.content,
                flags=0 if au.data.case_sensitive else IGNORECASE
            )
        case AutoResponseMethod.mention:
            match = search(
                pattern=rf'<@!?{au.trigger}>(\s|$)',
                string=message.content,
                flags=0 if au.data.case_sensitive else IGNORECASE
            )
        case AutoResponseMethod.disabled:
            return 'Auto response is disabled'
        case _:
            return f'Unknown method: {au.method}'

    if match is None:
        return 'No match'

    if au.data.nsfw and not message.channel.nsfw:
        return 'Auto response is nsfw and channel is not nsfw'

    if au.data.user is not None and message.author.id != au.data.user:
        return 'User does not match'

    if au.data.guild is not None and message.guild.id != au.data.guild:
        return 'Guild does not match'

    match au.type:
        case AutoResponseType.text:
            return f'Successful text response:\n{au.response}'
        case AutoResponseType.file:
            return 'File responses are not supported in the test environment'
        case AutoResponseType.script:
            try:
                on_message: Callable = import_module(
                    f'auto_responses.{au.response}').on_message
            except ImportError:
                return f'Failed to import script {au.response}'

            try:
                st = perf_counter()
                response: Response | None = on_message(message)
                et = perf_counter()
            except Exception as e:
                return f'Failed to execute script {au.response}: {e}'

            if et-st > 5:
                return f'Script execution took longer than 5 seconds: {et-st:.2f}s'

            if response is None:
                return 'No response from script'

            success_message = f'Successful script response (execution time: {(et-st)*1000:.2f}ms)'

            if response.file:
                return 'File responses are not supported in the test environment'

            if response.content and response.embeds:
                return 'Script returned both content and embeds'

            if response.embeds and response.followups:
                return 'Script returned both embeds and followups'

            if response.content:
                success_message += f'\nresponse text: {response.content}'

            if response.embeds:
                for embed in response.embeds:
                    embed.validate()

                embeds = '\n'.join((str(embed) for embed in response.embeds))
                success_message += f'response embeds:\n{embeds}'

            if response.followups:
                followups = '\n'.join(
                    (followup.response for followup in response.followups))
                success_message += f'response followups:\n{followups}'

            return success_message

        case AutoResponseType.deleted:
            return 'Auto response has been deleted'
        case _:
            return f'Unknown type: {au.type}'
