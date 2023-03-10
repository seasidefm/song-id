""" The main entrypoint for the song id api """

import logging
from logging.config import dictConfig

import dotenv
from fastapi import FastAPI

from config import LogConfig
from stream_watcher import StreamWatcher, JobResult
from utils.ffmpeg import convert_mp4_to_mp3

dotenv.load_dotenv()

# Init logger

dictConfig(LogConfig().dict())
logger = logging.getLogger("song-id")

# app = FastAPI(lifespan=lifespan)
app = FastAPI()


@app.get("/")
def ger_health():
    """ Simple health check route """
    return "OK"


@app.get("/identify/{creator}")
async def get_song_from_creator(creator: str):
    """ Identify a song based on creator name """
    logger.info("Song ID request for %s", creator)

    watcher = StreamWatcher()

    retry_count = 0
    while retry_count < 3:
        result = await watcher.run(creator)

        # Short circuit if we failed
        if result.result != JobResult.SUCCESS:
            logger.info("Stream watcher failed to get stream for %s! Retrying...", creator)
            retry_count += 1
            continue

        formatted_file = convert_mp4_to_mp3(result.data.get("file_name", None))
        song_id = await watcher.get_song_id(formatted_file)

        # Short circuit again if we failed
        if song_id is None:
            logger.info("Could not get a song match for %s! Retrying...", creator)
            watcher.cleanup(creator)
            retry_count += 1
            continue

        watcher.cleanup(creator, True)
        return song_id

    return {"error": "Could not get a song match!"}
