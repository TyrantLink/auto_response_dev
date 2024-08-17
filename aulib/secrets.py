from tomllib import loads
from dataclasses import dataclass
from os.path import exists

# ? update this dataclass to match the secrets you need, always set a default value of None


@dataclass
class Secrets:
    github_token: str | None = None
    gitlab_token: str | None = None


if not exists('secrets.toml'):
    with open('secrets.toml', 'w') as f:
        f.write(
            '''
            # fill in or create needed secrets
            # note: if creating secrets, be sure to add them to aulib.secrets.py and
            '''.replace('    ', '')
        )


with open('secrets.toml') as f:
    SECRETS = Secrets(**loads(f.read()))
