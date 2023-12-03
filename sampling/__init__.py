from typing import TypeAlias, Literal

from sampling.StreamlinkSource import StreamlinkSource

SupportedPlatform: TypeAlias = Literal["twitch"]


class UnsupportedPlatform(Exception):
    pass


class Sampler:
    def __init__(self, platform: SupportedPlatform, creator: str):
        self.platform = platform
        self.creator = creator

    def sample(self, duration: int):
        match self.platform:
            case "twitch":
                source = StreamlinkSource(f"https://twitch.tv/{self.creator}", duration)
            case other:
                raise UnsupportedPlatform(other)

        source.prepare()
        return source.get_sample()
