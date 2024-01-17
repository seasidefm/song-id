import logging
import os
from urllib import parse as urllib
from typing import TypeAlias, Literal, Any, Coroutine

from processing.ffmpeg_processor import FfmpegProcessor
from sampling.StreamlinkSource import StreamlinkSource

SupportedPlatform: TypeAlias = Literal["twitch", "youtube"]


logger = logging.getLogger("song-id")


class UnsupportedPlatform(Exception):
    pass


class Processor:
    def __init__(self, remove_after_processing: bool):
        self.remove_after_processing = remove_after_processing

    async def process(self, mp4_path: str) -> str | None:
        if mp4_path is None or not mp4_path.endswith(".mp4"):
            logger.error("Invalid mp4 path: %s", mp4_path)
            return None

        try:
            processed_file = await FfmpegProcessor().process(mp4_path, mp4_path.replace(".mp4", ".mp3"))

            if self.remove_after_processing:
                os.remove(mp4_path)

            return processed_file

        except Exception as e:
            logger.error("Failed to process %s: %s", mp4_path, e)
            logger.error("Error class: %s", e.__class__)
            return None
