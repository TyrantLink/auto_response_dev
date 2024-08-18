from dataclasses import dataclass, field


@dataclass
class EmbedFooter:
    text: str
    icon_url: str | None = None
    proxy_icon_url: str | None = None

    def to_dict(self) -> dict:
        return {
            'text': self.text,
            'icon_url': self.icon_url,
            'proxy_icon_url': self.proxy_icon_url
        }


@dataclass
class EmbedImage:
    url: str
    proxy_url: str | None = None
    height: int | None = None
    width: int | None = None

    def to_dict(self) -> dict:
        return {
            'url': self.url,
            'proxy_url': self.proxy_url,
            'height': self.height,
            'width': self.width
        }


@dataclass
class EmbedThumbnail:
    url: str
    proxy_url: str | None = None
    height: int | None = None
    width: int | None = None

    def to_dict(self) -> dict:
        return {
            'url': self.url,
            'proxy_url': self.proxy_url,
            'height': self.height,
            'width': self.width
        }


@dataclass
class EmbedVideo:
    url: str
    height: int | None = None
    width: int | None = None

    def to_dict(self) -> dict:
        return {
            'url': self.url,
            'height': self.height,
            'width': self.width
        }


@dataclass
class EmbedProvider:
    name: str | None = None
    url: str | None = None

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'url': self.url
        }


@dataclass
class EmbedAuthor:
    name: str
    url: str | None = None
    icon_url: str | None = None
    proxy_icon_url: str | None = None

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'url': self.url,
            'icon_url': self.icon_url,
            'proxy_icon_url': self.proxy_icon_url
        }


@dataclass
class EmbedField:
    name: str
    value: str
    inline: bool | None = False

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'value': self.value,
            'inline': self.inline
        }


@dataclass
class Embed:
    title: str | None = None
    type: str | None = 'rich'
    description: str | None = None
    url: str | None = None
    color: int | None = None
    footer: EmbedFooter | None = None
    image: EmbedImage | None = None
    thumbnail: EmbedThumbnail | None = None
    video: EmbedVideo | None = None
    provider: EmbedProvider | None = None
    author: EmbedAuthor | None = None
    fields: list[EmbedField] = field(default_factory=list)

    def validate(self) -> None:
        total_chars = 0

        if self.title:
            total_chars += len(self.title)
            if len(self.title) > 256:
                raise ValueError('title must be less than 256 characters')

        if self.description:
            total_chars += len(self.description)
            if len(self.description) > 4096:
                raise ValueError(
                    'description must be less than 4096 characters')

        if self.fields and len(self.fields) > 25:
            raise ValueError('embed must have less than 25 fields')

        for field in self.fields:
            total_chars += len(field.name) + len(field.value)

            if len(field.name) > 256:
                raise ValueError('field name must be less than 256 characters')

            if len(field.value) > 1024:
                raise ValueError(
                    'field value must be less than 1024 characters')

        if self.footer:
            total_chars += len(self.footer.text)

            if len(self.footer.text) > 2048:
                raise ValueError(
                    'footer text must be less than 2048 characters')

        if self.author:
            total_chars += len(self.author.name)

            if len(self.author.name) > 256:
                raise ValueError(
                    'author name must be less than 256 characters')

        if total_chars > 6000:
            raise ValueError(
                'total characters in embed must be less than 6000')

    def to_dict(self) -> dict:
        return {
            k: (v.to_dict() if hasattr(v, 'to_dict') else v)
            for k, v
            in self.__dict__.items()
            if v is not None
        }
