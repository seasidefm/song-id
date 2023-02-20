from datetime import datetime

import dotenv
import os
from fastapi import FastAPI
from shazamio import Shazam

from utils.streamlink import get_stream_from_creator
from utils.ffmpeg import convert_mp4_to_mp3

dotenv.load_dotenv()

app = FastAPI()


@app.get("/")
def ger_health():
    return "OK"


@app.get("/identify/{creator}")
async def get_song_from_creator(creator: str):
    print(f"Received song ID request for {creator}")
    start_time = datetime.utcnow().timestamp()
    created_file = get_stream_from_creator(creator)
    formatted_file = convert_mp4_to_mp3(created_file)

    shazam = Shazam()
    out = await shazam.recognize_song(formatted_file)

    # Cleanup
    os.remove(created_file)
    os.remove(formatted_file)

    end_time = datetime.utcnow().timestamp()

    print(f"Handled song id in {end_time - start_time}s")

    return out
