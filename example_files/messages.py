from auto_responses.lib.models import Message, Channel, Guild, User
from datetime import datetime


# ? if True, test with COMPLEX_TEST_MESSAGES, else test with SIMPLE_TEST_MESSAGES
TEST_COMPLEX = False


# ? test with just the message content
SIMPLE_TEST_MESSAGES = [
    'unset test message'
]

# ? or uncomment to test with full context
COMPLEX_TEST_MESSAGES = [
    Message(
        id=0,
        author=User(
            name='unset',
            id=0,
            created_at=datetime.now(),
            nickname='unset'
        ),
        channel=Channel(
            name='unset',
            id=0,
            nsfw=False
        ),
        guild=Guild(
            name='unset',
            id=0,
            me=User(
                name='/reg/nal',
                id=1,
                created_at=datetime.now(),
                nickname='/reg/nal'
            )
        ),
        content='unset'
    )
]

if TEST_COMPLEX:
    TEST_MESSAGES = COMPLEX_TEST_MESSAGES
else:
    TEST_MESSAGES = [
        Message(
            id=0,
            author=User(
                name='unset',
                id=0,
                created_at=datetime.now(),
                nickname='unset'
            ),
            channel=Channel(
                name='unset',
                id=0,
                nsfw=False
            ),
            guild=Guild(
                name='unset',
                id=0,
                me=User(
                    name='/reg/nal',
                    id=1,
                    created_at=datetime.now(),
                    nickname='/reg/nal'
                )
            ),
            content=content
        )
        for content in SIMPLE_TEST_MESSAGES
    ]
