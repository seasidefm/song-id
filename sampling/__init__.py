import logging
from urllib import parse as urllib
from typing import TypeAlias, Literal

from sampling.StreamlinkSource import StreamlinkSource

SupportedPlatform: TypeAlias = Literal["twitch", "youtube"]


logger = logging.getLogger("song-id")


class UnsupportedPlatform(Exception):
    pass


class Sampler:
    def __init__(self, platform: SupportedPlatform, creator: str):
        self.platform = platform
        self.creator = creator

    def sample(self, duration: int):
        try:
            match self.platform:
                case "twitch":
                    source = StreamlinkSource(
                        f"https://twitch.tv/{self.creator}", "twitch", duration
                    )
                case "youtube":
                    decoded_url = urllib.unquote(self.creator).replace('"', "")
                    source = StreamlinkSource(decoded_url, "youtube", duration)
                case other:
                    raise UnsupportedPlatform(other)

            source.prepare()
            return source.get_sample()
        except Exception as e:
            logger.error("Failed to get sample for %s: %s", self.creator, e)
            logger.error("Error class: %s", e.__class__)
            return None
