# mildly based on https://github.com/dolphingarlic/git-the-lines
from ...aulib import ScriptAuthor, Message, Response
from re import compile
from .fetch import (
    fetch_github_snippet,
    # fetch_github_gist_snippet,
    # fetch_gitlab_snippet,
    # fetch_bitbucket_snippet,
    # fetch_heptapod_snippet
)

author = ScriptAuthor(
    name='tyrantlink',
    id=250797109022818305
)


GITHUB = compile(
    r'https://github\.com/(?P<repo>[a-zA-Z0-9-]+/[\w.-]+)/blob/'
    r'(?P<path>[^#>\s]+)(\?[^#>\s]+)?(#L(?P<start_line>\d+)([-~:]L(?P<end_line>\d+))?)?'
)

# GITHUB_GIST = compile(
#     r'https://gist\.github\.com/([a-zA-Z0-9-]+)/(?P<gist_id>[a-zA-Z0-9]+)/*'
#     r'(?P<revision>[a-zA-Z0-9]*)/*#file-(?P<file_path>[^#>\s]+?)(\?[^#>\s]+)?'
#     r'(-L(?P<start_line>\d+)([-~:]L(?P<end_line>\d+))?)'
# )

# GITLAB = compile(
#     r'https://gitlab\.com/(?P<repo>[\w.-]+/[\w.-]+)/\-/blob/(?P<path>[^#>\s]+)'
#     r'(\?[^#>\s]+)?(#L(?P<start_line>\d+)(-(?P<end_line>\d+))?)?'
# )

# BITBUCKET = compile(
#     r'https://bitbucket\.org/(?P<repo>[a-zA-Z0-9-]+/[\w.-]+)/src/(?P<ref>[0-9a-zA-Z]+)'
#     r'/(?P<file_path>[^#>\s]+)(\?[^#>\s]+)?(#lines-(?P<start_line>\d+)(:(?P<end_line>\d+))?)?'
# )

# HEPTAPOD = compile(
#     r'https://foss\.heptapod\.net/(?P<repo>[a-zA-Z0-9-]+/[\w.-]+)/-/blob/branch/'
#     r'(?P<path>[^#>]+)(\?[^#>]+)?(#L(?P<start_line>\d+)([-~:](?P<end_line>\d+))?)?'
# )

pattern_handlers = {
    GITHUB: fetch_github_snippet,
    # GITHUB_GIST: fetch_github_gist_snippet,
    # GITLAB: fetch_gitlab_snippet,
    # BITBUCKET: fetch_bitbucket_snippet,
    # HEPTAPOD: fetch_heptapod_snippet
}


def on_message(message: Message) -> Response | None:
    response = '\n'.join(
        [
            content
            for pattern, handler in pattern_handlers.items()
            for match in pattern.finditer(message.content)
            if (content := handler(**match.groupdict())) is not None
        ]
    )
    if not response:
        return None

    if len(response) > 2000:
        return Response(content=f'snippet too long ({len(response)}/2000)')

    return Response(content=response)
