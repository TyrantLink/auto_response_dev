from contextlib import redirect_stdout, redirect_stderr
from aulib import ScriptAuthor, Message, Response
from traceback import format_exc
from io import StringIO

author = ScriptAuthor(
    name='tyrantlink',
    id=250797109022818305
)


def on_message(message: Message) -> Response | None:
    # ? temporary hardcode until i make this safer
    if message.author.id != 250797109022818305:
        return Response(content='not until i make this safer')

    code = '\n'.join(message.content.split('\n')[2:-1])

    with StringIO() as output:
        with redirect_stdout(output), redirect_stderr(output):
            try:
                exec(code, {}, {})
            except Exception as e:
                err = format_exc().splitlines()
                del err[1]  # file path
                del err[1]  # exec(code)
                err[1] = err[1].replace('<string>', '<stdin>')
                print('\n'.join(err))

        captured_output = output.getvalue()

    return Response(
        content=f'```\n{captured_output}\n```' if captured_output else 'no output',
    )
