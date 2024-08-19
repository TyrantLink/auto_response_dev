from pydantic.main import BaseModel
from requests import get as _get
from aulib import SECRETS
from textwrap import dedent
from json import loads


class HTTPResponse(BaseModel):
    name: str


def get(url: str, **kwargs) -> str:
    response = _get(url, **kwargs)
    if response.status_code != 200:
        raise Exception(f'Failed to fetch {url}: {response.status_code}')
    # print(f'{url}:{response.status_code}:{response.text}')
    return response.text


def fetch_github_snippet(repo: str, path: str, start_line: str, end_line: str) -> str | None:
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    if SECRETS.github_token is not None:
        headers['Authorization'] = f'token {SECRETS.github_token}'

    refs = (
        [
            HTTPResponse.model_validate(j)
            for j in loads(get(
                f'https://api.github.com/repos/{repo}/branches',
                headers=headers
            ))
        ] +
        [
            HTTPResponse.model_validate(j)
            for j in loads(get(
                f'https://api.github.com/repos/{repo}/tags',
                headers=headers
            ))
        ]
    )

    ref, file_path = path.split('/', 1) if '/' in path else (path, '')

    for possible_ref in refs:
        if path.startswith(f'{possible_ref.name}/'):
            ref = possible_ref.name
            file_path = path[len(ref) + 1:]
            break

    file_contents = get(
        f'https://api.github.com/repos/{repo}/contents/{file_path}?ref={ref}',
        headers=headers
    )

    if file_contents is None:
        return None

    return to_text(
        file_contents,
        file_path,
        start_line,
        end_line,
        f'https://github.com/{repo}/blob/{ref}/{file_path}',
        repo,
        f'https://github.com/{repo}'
    )


#! all still copied from https://github.com/dolphingarlic/git-the-lines, i'll implement them later
# def fetch_github_gist_snippet(session, gist_id, revision, file_path, start_line, end_line):
#     """Fetches a snippet from a gist"""

#     headers = {'Accept': 'application/vnd.github.v3.raw'}
#     if "GITHUB_TOKEN" in os.environ:
#         headers['Authorization'] = f'token {os.environ["GITHUB_TOKEN"]}'

#     gist_json = fetch_http(
#         session,
#         f'https://api.github.com/gists/{gist_id}{f"/{revision}" if len(revision) > 0 else ""}',
#         'json',
#         headers=headers,
#     )

#     for gist_file in gist_json['files']:
#         if file_path == gist_file.lower().replace('.', '-'):
#             file_contents = fetch_http(
#                 session,
#                 gist_json['files'][gist_file]['raw_url'],
#                 'text',
#             )

#             return snippet_to_embed(file_contents, gist_file, start_line, end_line)

#     return ''


# def fetch_gitlab_snippet(session, repo, path, start_line, end_line):
#     """Fetches a snippet from a gitlab repo"""

#     headers = {}
#     if 'GITLAB_TOKEN' in os.environ:
#         headers['PRIVATE-TOKEN'] = os.environ['GITLAB_TOKEN']

#     enc_repo = quote_plus(repo)

#     refs = (fetch_http(session, f'https://gitlab.com/api/v4/projects/{enc_repo}/repository/branches', 'json', headers=headers) +
#             fetch_http(session, f'https://gitlab.com/api/v4/projects/{enc_repo}/repository/tags', 'json', headers=headers))

#     ref = path.split('/')[0]
#     file_path = '/'.join(path.split('/')[1:])
#     for possible_ref in refs:
#         if path.startswith(possible_ref['name'] + '/'):
#             ref = possible_ref['name']
#             file_path = path[len(ref) + 1:]
#             break

#     enc_ref = quote_plus(ref)
#     enc_file_path = quote_plus(file_path)

#     file_contents = fetch_http(
#         session,
#         f'https://gitlab.com/api/v4/projects/{enc_repo}/repository/files/{enc_file_path}/raw?ref={enc_ref}',
#         'text',
#         headers=headers,
#     )

#     return snippet_to_embed(file_contents, file_path, start_line, end_line)


# def fetch_bitbucket_snippet(session, repo, ref, file_path, start_line, end_line):
#     """Fetches a snippet from a bitbucket repo"""

#     file_contents = fetch_http(
#         session,
#         f'https://bitbucket.org/{quote_plus(repo)}/raw/{quote_plus(ref)}/{quote_plus(file_path)}',
#         'text',
#     )

#     return snippet_to_embed(file_contents, file_path, start_line, end_line)


# def fetch_heptapod_snippet(session, repo, path, start_line, end_line):
#     file_contents = fetch_http(
#         session,
#         f'https://foss.heptapod.net/{repo}/-/raw/branch/{path}',
#         'text',
#     )

#     file_path = '/'.join(path.split('/')[1:])
#     return snippet_to_embed(file_contents, file_path, start_line, end_line)


def to_text(
    file_contents: str,
    file_path: str,
    start: str,
    end: str,
    url: str,
    repo: str,
    repo_url: str
) -> str | None:
    """Given file contents, file path, start line and end line creates a code block"""

    split_file_contents = file_contents.splitlines()
    start_line = int(start) if start is not None else None
    end_line = int(end) if end is not None else None

    if start_line is None:
        start_line, end_line = 1, len(split_file_contents)
    if end_line is None:
        start_line = end_line = start_line

    if start_line > end_line:
        start_line, end_line = end_line, start_line
    if start_line > len(split_file_contents) or end_line < 1:
        return None

    start_line = max(1, start_line)
    end_line = min(len(split_file_contents), end_line)

    required = dedent('\n'.join(
        split_file_contents[start_line - 1:end_line])).rstrip().replace('`', '`\u200b')

    language = file_path.split('/')[-1].split('.')[-1]
    if not language.translate(str.maketrans('', '', '-+_')).isalnum():
        language = ''

    ret = (
        f'`{file_path}` line {start_line}'
        if start_line == end_line
        else f'`{file_path}` lines {start_line} to {end_line}'
    )

    if not len(required):
        return None

    return f'[`{repo}`](<{repo_url}>)\n[{ret}](<{url}>)\n```{language}\n{required}```'
