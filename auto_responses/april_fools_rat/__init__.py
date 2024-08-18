from ...aulib import ScriptAuthor, Message, Response
from datetime import datetime

author = ScriptAuthor(
    name='tyrantlink',
    id=250797109022818305
)


def on_message(message: Message) -> Response | None:
    if not all((
        datetime.now().month == 4,
        datetime.now().day == 1
    )):
        return None

    if 'rat' in message.content.lower():
        return Response(file='rat.png')

    return None
