# created by tyrantlink
from ...aulib import Message, Response
from datetime import datetime


def on_message(message: Message) -> Response | None:
    if not all((
        datetime.now().month == 4,
        datetime.now().day == 1
    )):
        return None

    if 'rat' in message.content.lower():
        return Response(file='rat.png')

    return None
