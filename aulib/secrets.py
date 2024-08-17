from tomllib import loads
from dataclasses import dataclass
from os.path import exists

# ? update this dataclass to match the secrets you need, always set a default value of None

_SECRETS_PATH = 'au_scripts/secrets.toml' if __name__ == 'au_scripts.aulib.secrets' else 'secrets.toml'


@dataclass
class Secrets:
    github_token: str | None = None
    gitlab_token: str | None = None


if not exists(_SECRETS_PATH):
    with open(_SECRETS_PATH, 'w') as f:
        f.write(
            '''
            # fill in or create needed secrets
            # note: if creating secrets, be sure to add them to aulib.secrets.py and
            '''.replace('    ', '').strip()
        )


with open(_SECRETS_PATH, 'r') as f:
    SECRETS = Secrets(**loads(f.read()))
