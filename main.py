""" The main entrypoint for the song id api """
import json
import os
from contextlib import asynccontextmanager
from datetime import datetime
from queue import Queue

import dotenv
from fastapi import FastAPI
from shazamio import Shazam

from stream_watcher import StreamWatcher, JobResult
from utils.acr_cloud import acr_identify
from utils.audd import audd_recognize_song
from utils.audd_class import AuddResponse
from utils.streamlink import get_stream_from_creator
from utils.ffmpeg import convert_mp4_to_mp3

dotenv.load_dotenv()

# Create a queue for the stream watcher
queue = Queue()


# @asynccontextmanager
# async def lifespan(_):
#     """ The lifespan context manager for the FastAPI app """
#     stream_watcher = StreamWatcher(queue)
#     stream_watcher.start()
#
#     yield
#
#     stop_job = StreamJob(
#         job_id=1,
#         job_type=JobType.STOP,
#         job_data={}
#     )
#
#     # Stop the stream watcher
#     queue.put(stop_job)


# app = FastAPI(lifespan=lifespan)
app = FastAPI()


@app.get("/")
def ger_health():
    """ Simple health check route """
    return "OK"


@app.get("/identify/{creator}")
async def get_song_from_creator(creator: str):
    """ Identify a song based on creator name """
    print(f"Received song ID request for {creator}")

    watcher = StreamWatcher()

    retry_count = 0
    while retry_count < 3:
        result = await watcher.run(creator)

        # Short circuit if we failed
        if result.result != JobResult.SUCCESS:
            print(f"Stream watcher failed to get stream for {creator}! Retrying...")
            retry_count += 1
            continue

        formatted_file = convert_mp4_to_mp3(result.data.get("file_name", None))
        id = await watcher.get_song_id(formatted_file)

        # Short circuit again if we failed
        if id is None:
            print("Could not get a song match! Retrying...")
            watcher.cleanup(creator)
            retry_count += 1
            continue

        watcher.cleanup(creator, True)
        return id

    return {"error": "Could not get a song match!"}
