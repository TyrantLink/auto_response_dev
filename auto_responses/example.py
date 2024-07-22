# created by YOUR_GITHUB_USERNAME
from models import Message
import time


def on_message(message: Message) -> str | None:
    return f'responding to {message.content} at {time.time()}'
