# created by YOUR_GITHUB_USERNAME
from ...aulib import Message, Response
import time


def on_message(message: Message) -> Response | None:
    return Response(
        content=f'responding to {message.content} at {time.time()}'
    )
