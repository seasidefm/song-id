""" Stream watcher module. """
import asyncio
import logging
from os import getenv
from enum import Enum
from typing import Union

from fs.osfs import OSFS
from pydantic import BaseModel
from shazamio import Shazam

from utils.audd import audd_recognize_song
from utils.audd_class import AuddResponse
from utils.streamlink import StreamFetcher


class JobResult(Enum):
    """Enum for the result of a job."""

    SUCCESS = 1
    FAILURE = 2


class JobOutput(BaseModel):
    """The result of a job that was processed by the stream watcher."""

    result: JobResult
    data: dict


class SongMatch(BaseModel):
    """The standardized result of a song match."""

    title: Union[str, None]
    artist: Union[str, None]
    link: Union[str, None]
    album: Union[str, None]


class StreamWatcher:
    """A thread that watches a queue for new stream monitor requests and processes them."""

    def __init__(self):
        temp_dir = getenv("TMP_DIR")

        if not temp_dir:
            raise ValueError("TMP_DIR environment variable is not set!")

        self.base_dir = temp_dir
        self.osfs = OSFS(self.base_dir)
        self.stream_link = StreamFetcher()
        self.stream_link.init_session()

        self.logger = logging.getLogger("song-id")

    async def run(self, creator: str) -> JobOutput:
        """Run the stream watcher"""
        self.logger.info("Starting stream watcher for %s", creator)

        try:
            file_name = f"{self.base_dir}/{creator}.mp4"

            self.stream_link.stream_via_cli(creator, file_name)

            return JobOutput(result=JobResult.SUCCESS, data={"file_name": file_name})

        except AttributeError as err:
            self.logger.error(
                "Stream watcher got a bad stream request for %s!", creator
            )
            self.logger.error(err)

            return JobOutput(result=JobResult.FAILURE, data={"error": str(err)})
        except Exception as err:
            self.logger.error("Stream watcher failed for %s!", creator)
            self.logger.error(err)

            return JobOutput(result=JobResult.FAILURE, data={"error": str(err)})

    async def get_song_id(self, file_name: str):
        """Get the song ID from the stream"""
        self.logger.info("Getting song ID for %s", file_name)

        shazam = Shazam(language="en-US")

        # Get all the song IDs from different services
        shazam_match = await asyncio.gather(
            shazam.recognize_song(file_name)
        )

        # Custom
        # =========

        # Audd.io
        # ========
        audd_song = SongMatch(title=None, artist=None, link=None)

        # if audd_id.get("error", None) is None:
        #     audd_result = AuddResponse(**audd_id)
        #     if audd_result.result is not None:
        #         audd_song = SongMatch(
        #             title=audd_result.result.get("title", None),
        #             artist=audd_result.result.get("artist", None),
        #             link=audd_result.result.get("song_link", None),
        #             album=audd_result.result.get("album", None),
        #         )

        # Shazam
        # ======

        # If NONE of the services returned a song, return None
        if (
            audd_song.title is None
            and shazam_match[0].get("track") is None
        ):
            return None

        return {"audd": audd_song.dict(), "shazam": shazam}

    def cleanup(self, creator: str, close_fs: bool = False):
        """Cleanup the stream watcher"""
        self.osfs.remove(f"{creator}.mp4")
        self.osfs.remove(f"{creator}.mp3")

        if close_fs:
            self.osfs.close()
