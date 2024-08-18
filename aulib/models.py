from dataclasses import dataclass
from .embed import Embed
from datetime import datetime
from enum import Enum


@dataclass
class User:
    name: str
    """user's global name."""
    id: int
    """user's discord id."""
    created_at: datetime
    """when the user was created."""
    nickname: str
    """user's nickname in the guild."""

    @property
    def display_name(self) -> str:
        """user's display name."""
        return self.nickname or self.name

    @property
    def mention(self) -> str:
        """user's mention string"""
        return f'<@{self.id}>'


@dataclass
class Channel:
    name: str
    """channel's name."""
    id: int
    """channel's discord id."""
    nsfw: bool
    """whether the channel is nsfw."""

    @property
    def mention(self) -> str:
        """channel's mention string"""
        return f'<#{self.id}>'


@dataclass
class Guild:
    name: str
    """guild's name."""
    id: int
    """guild's discord id."""
    me: User
    """bot's user object in the guild."""


@dataclass
class Attachment:
    filename: str
    """attachment filename."""
    url: str
    """attachment url."""
    proxy_url: str
    """attachment proxy url."""


@dataclass
class Message:
    id: int
    """message discord id."""
    author: User
    """message author."""
    channel: Channel
    """message channel."""
    guild: Guild
    """message guild."""
    content: str
    """message content."""
    attachments: list[Attachment]
    """list of attachments."""


@dataclass
class AutoResponseFollowup:
    delay: float
    """delay in seconds before sending followup."""
    response: str
    """followup response."""


class AutoResponseMethod(Enum):
    exact = 0
    """requires exact match of trigger."""
    contains = 1
    """requires trigger to be contained in message."""
    regex = 2
    """requires trigger to match regex pattern.\n
    NOTE: this method is different from AutoResponseData.regex
    this method does NOT use the standard word boundary regex"""
    mention = 3
    """trigger must be a numerical user id, only responds when user is mentioned."""
    disabled = 4
    """disables the autoresponse."""


class AutoResponseType(Enum):
    text = 0
    """response is text."""
    file = 1
    """response is a file hosted on api.regn.al."""
    script = 2
    """response is a script to be executed."""
    deleted = 3
    """auto response no longer exists."""


@dataclass
class AutoResponseData:
    weight: int
    """weight when randomly selecting a response. (only used when multiple auto responses are triggered)\n
    most base auto responses have a weight of 1000"""
    chance: float
    """chance of the auto response being triggered. (0.0 - 100.0)"""
    ignore_cooldown: bool
    """whether to ignore the auto response cooldown.
    NOTE: this can ONLY be set as a guild auto response override."""
    custom: bool
    """whether the auto response is a custom auto response."""
    regex: bool
    """whether the trigger is a regex pattern."""
    nsfw: bool
    """whether the auto response is nsfw.
    if True, the auto response will only trigger in nsfw channels."""
    case_sensitive: bool
    """whether the trigger is case sensitive."""
    delete_trigger: bool
    """whether to delete the trigger message.
    NOTE: this can ONLY be set as a guild auto response override."""
    reply: bool
    """whether to reply to the message that triggered the auto response."""
    suppress_trigger_embeds: bool
    """whether to suppress the trigger message's embeds."""
    user: int | None
    """if True, only this user can trigger the auto response."""
    guild: int | None
    """if True, this auto response can only be triggered in this guild."""
    source: str | None
    """source of the auto response."""
    followups: list[AutoResponseFollowup]
    """list of followups to send after the initial response. max 10 followups."""


@dataclass
class AutoResponse:
    id: str
    """MUST be unset, au is given an id when it is added to the database"""
    method: AutoResponseMethod
    trigger: str
    response: str
    """MUST be the name of the script folder"""
    type: AutoResponseType
    """MUST be AutoResponseType.script"""
    data: AutoResponseData


@dataclass
class ScriptAuthor:
    name: str
    """author's name."""
    id: int
    """author's discord id."""


@dataclass
class Response:
    content: str | None = None
    """response message content\n\nMUTUALLY EXCLUSIVE WITH file and embeds"""
    embeds: list[Embed] | None = None
    """list of embeds (up to 10)\n\nMUTUALLY EXCLUSIVE WITH content and file"""
    file: str | None = None
    """file name hosted on api.regn.al\n\nMUTUALLY EXCLUSIVE WITH content and embeds"""
    followups: list[AutoResponseFollowup] | None = None
    """list of followups to send after the initial response. Max 10 followups.\n\nMUTUALLY EXCLUSIVE WITH embeds and file"""
