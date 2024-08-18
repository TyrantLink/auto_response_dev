from dataclasses import dataclass
from .embed import Embed
from datetime import datetime
from enum import Enum


@dataclass
class User:
    name: str
    """User's global name."""
    id: int
    """User's discord id."""
    created_at: datetime
    """When the user was created."""
    nickname: str
    """User's nickname in the guild."""

    @property
    def display_name(self) -> str:
        """User's display name."""
        return self.nickname or self.name

    @property
    def mention(self) -> str:
        """User's mention string"""
        return f'<@{self.id}>'


@dataclass
class Channel:
    name: str
    """Channel's name."""
    id: int
    """Channel's discord id."""
    nsfw: bool
    """Whether the channel is nsfw."""

    @property
    def mention(self) -> str:
        """Channel's mention string"""
        return f'<#{self.id}>'


@dataclass
class Guild:
    name: str
    """Guild's name."""
    id: int
    """Guild's discord id."""
    me: User
    """Bot's user object in the guild."""


@dataclass
class Message:
    id: int
    """Message discord id."""
    author: User
    """Message author."""
    channel: Channel
    """Message channel."""
    guild: Guild
    """Message guild."""
    content: str
    """Message content."""


@dataclass
class AutoResponseFollowup:
    delay: float
    """Delay in seconds before sending followup."""
    response: str
    """Followup response."""


class AutoResponseMethod(Enum):
    exact = 0
    """Requires exact match of trigger."""
    contains = 1
    """Requires trigger to be contained in message."""
    regex = 2
    """Requires trigger to match regex pattern.
    NOTE: This method is different from AutoResponseData.regex
    This method does NOT use the standard word boundary regex"""
    mention = 3
    """Trigger must be a numerical user id, only responds when user is mentioned."""
    disabled = 4
    """Disables the autoresponse."""


class AutoResponseType(Enum):
    text = 0
    """Response is text."""
    file = 1
    """Response is a file hosted on api.regn.al."""
    script = 2
    """Response is a script to be executed."""
    deleted = 3
    """Auto Response no longer exists."""


@dataclass
class AutoResponseData:
    weight: int
    """Weight when randomly selecting a response. (only used when multiple auto responses are triggered)
    Most base auto responses have a weight of 1000"""
    chance: float
    """Chance of the auto response being triggered. (0.0 - 100.0)"""
    ignore_cooldown: bool
    """Whether to ignore the auto response cooldown.
    NOTE: this can ONLY be set as a guild auto response override."""
    custom: bool
    """Whether the auto response is a custom auto response."""
    regex: bool
    """Whether the trigger is a regex pattern."""
    nsfw: bool
    """Whether the auto response is nsfw.
    if True, the auto response will only trigger in nsfw channels."""
    case_sensitive: bool
    """Whether the trigger is case sensitive."""
    delete_trigger: bool
    """Whether to delete the trigger message.
    NOTE: this can ONLY be set as a guild auto response override."""
    reply: bool
    """Whether to reply to the message that triggered the auto response."""
    suppress_trigger_embeds: bool
    """Whether to suppress the trigger message's embeds."""
    user: int | None
    """if True, only this user can trigger the auto response."""
    guild: int | None
    """if True, this auto response can only be triggered in this guild."""
    source: str | None
    """Source of the auto response."""
    followups: list[AutoResponseFollowup]
    """List of followups to send after the initial response. Max 10 followups."""


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
