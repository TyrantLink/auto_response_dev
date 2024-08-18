from ...aulib import ScriptAuthor, Message, Response
import time

author = ScriptAuthor(
    name='your_discord_username',
    id=0
)


def on_message(message: Message) -> Response | None:
    return Response(
        content=f'responding to {message.content} at {time.time()}'
    )
