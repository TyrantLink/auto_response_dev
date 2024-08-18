from regex import sub, split, finditer, IGNORECASE
from ...aulib import ScriptAuthor, Message, Response
from random import choices

author = ScriptAuthor(
    name='tyrantlink',
    id=250797109022818305
)


def rand_name(message: Message, splitter: str) -> str:
    options = [message.guild.me.display_name]
    weights: list[float] = []

    if splitter in ["i'm"]:
        options += ['proud of you', 'not mad, just disappointed']
        weights += [0.005, 0.01]

    # ? mypyc isn't happy if this is part of weights.insert
    weight_sum = sum(weights)
    weights.insert(0, 1-weight_sum)

    return choices(options, weights)[0]


def on_message(message: Message) -> Response | None:
    response, splitter = '', ''
    input = sub(r'<(@!|@|@&)\d{10,25}>|@everyone|@here|(https?:\/\/[^\s]+.)', '[REDACTED]', sub(
        r'\*|\_|\~|\`|\|', '', message.content))
    splitters = "i'm|im|i am|i will be|i've|ive"

    for s in finditer(splitters, input, IGNORECASE):
        if (
            s is None or
            (s.span()[0] != 0 and input[s.span()[0]-1] != ' ') or
                (s.span()[1] < len(input) and input[s.span()[1]] != ' ')):
            continue
        response = ''.join(
            split(
                pattern=s.captures()[0],
                string=input,
                maxsplit=1,
                flags=IGNORECASE
            )[1:])
        splitter = s.captures()[0].lower()

    if response == '':
        return None
    name = rand_name(message, splitter)

    nl = '\n'  # ? python stupid
    response = f'hi{split(f"[,.;{nl}]", response)[0]}, {splitter} {name}'

    if len(response) > 2000:
        return None

    return Response(content=response)
