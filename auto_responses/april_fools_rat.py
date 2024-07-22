# created by tyrantlink
from models import Message
from datetime import datetime


def on_message(message: Message) -> str | None:
    if not (datetime.now().month == 4 and datetime.now().day == 1):
        return None

    if 'rat' in message.content.lower():
        return 'rat.png'

    return None
