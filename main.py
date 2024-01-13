""" The main entrypoint for the song id api """
import datetime

import base64

import logging
from logging.config import dictConfig

import dotenv
from fastapi import FastAPI

from matcher import Matcher
from config import LogConfig
from sampling import Sampler, SupportedPlatform

dotenv.load_dotenv()

# Init logger

dictConfig(LogConfig().dict())
logger = logging.getLogger("song-id")

# app = FastAPI(lifespan=lifespan)
app = FastAPI()


@app.get("/health")
def get_health():
    """Simple health check route"""
    return {"status": "ok"}


@app.get("/sample")
async def get_sample_from_creator(
    creator: str, platform: SupportedPlatform = "twitch", duration: int = 7
):
    logger.info("Sample request for %s", creator)

    sampler = Sampler(platform, creator)
    sample_file = sampler.sample(duration)

    if sample_file is None:
        return {"error": "Failed to get sample"}

    return {
        "creator": creator,
        "duration": duration,
        "timestamp": int(datetime.datetime.utcnow().timestamp()),
        "data": base64.b64encode(open(sample_file, "rb").read()),
    }


@app.get("/identify")
async def get_song_from_creator(
    creator: str, platform: SupportedPlatform = "twitch", duration: int = 7
):
    """Identify a song based on creator name"""
    logger.info("Song ID request for %s", creator)

    sampler = Sampler(platform, creator)
    matcher = Matcher()

    sample_file = sampler.sample(duration)
    if sample_file is None:
        return {"error": "Failed to get sample"}

    match = await matcher.match(sample_file)

    return match

    # watcher = StreamWatcher()

    # retry_count = 0
    # while retry_count < 3:
    # result = await watcher.run(creator)

    #     # Short circuit if we failed
    #     if result.result != JobResult.SUCCESS:
    #         logger.info(
    #             "Stream watcher failed to get stream for %s! Retrying...", creator
    #         )
    #         retry_count += 1
    #         continue
    #
    #     formatted_file = convert_mp4_to_mp3(result.data.get("file_name", None))
    #     song_id = await watcher.get_song_id(formatted_file)
    #
    #     # Short circuit again if we failed
    #     if song_id is None:
    #         logger.info("Could not get a song match for %s! Retrying...", creator)
    #         watcher.cleanup(creator)
    #         retry_count += 1
    #         continue
    #
    #     watcher.cleanup(creator, True)
    #     return song_id
    #
    # return {"error": "Could not get a song match!"}
