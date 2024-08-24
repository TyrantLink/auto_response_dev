from RestrictedPython.Guards import safer_getattr, guarded_iter_unpack_sequence, guarded_unpack_sequence
from RestrictedPython.Eval import default_guarded_getitem, default_guarded_getiter
from RestrictedPython import compile_restricted, safe_builtins
from contextlib import redirect_stdout, redirect_stderr
from aulib import ScriptAuthor, Message, Response
from traceback import format_exc
from io import StringIO


author = ScriptAuthor(
    name='tyrantlink',
    id=250797109022818305
)


class Print:
    def __init__(self, _getattr_=None):
        ...

    def _call_print(self, *objects, **kwargs):
        kwargs.pop('file', None)
        print(*objects, **kwargs)


safe_globals = {
    '__builtins__': safe_builtins,
    '_print_': Print,
    'getattr': safer_getattr,
    '__name__': '__main__',
    'token': 'what, do you think i\'m an idiot?',
    '_getitem_': default_guarded_getitem,
    '_getiter_': default_guarded_getiter,
    '_iter_unpack_sequence_': guarded_iter_unpack_sequence,
    '_unpack_sequence_': guarded_unpack_sequence
}


def on_message(message: Message) -> Response | None:

    unsafe = False
    if message.content.splitlines()[1] == '#!/reg/nal-unsafe':
        if message.author.id != author.id:
            return Response(
                content='not allowed :3'
            )
        unsafe = True

    code = '\n'.join(message.content.split('\n')[2:-1])

    with StringIO() as compiler_output:
        with redirect_stdout(compiler_output), redirect_stderr(compiler_output):
            try:
                if unsafe:
                    compile(code, '<stdin>', 'exec')
                else:
                    code = compile_restricted(code, '<stdin>')
            except:
                err = format_exc().splitlines()
                return Response(
                    content='\n'.join(err)
                )

    with StringIO() as output:
        with redirect_stdout(output), redirect_stderr(output):
            try:
                if unsafe:
                    exec(code)
                else:
                    exec(code, safe_globals, {})
            except:  # ? catch *every* exception
                err = format_exc().splitlines()
                del err[1]  # file path
                del err[1]  # exec
                err[1] = err[1].replace('<string>', '<stdin>')
                print('\n'.join(err))

        captured_output = output.getvalue()

    return Response(
        content=f'```\n{captured_output}\n```' if captured_output else 'no output',
    )
