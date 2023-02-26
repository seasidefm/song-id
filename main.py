""" The main entrypoint for the song id api """
import json
import os
from datetime import datetime

import dotenv
from fastapi import FastAPI
from shazamio import Shazam

from utils.acr_cloud import acr_identify
from utils.audd import audd_recognize_song
from utils.audd_class import AuddResponse
from utils.streamlink import get_stream_from_creator
from utils.ffmpeg import convert_mp4_to_mp3

dotenv.load_dotenv()

app = FastAPI()


@app.get("/")
def ger_health():
    """ Simple health check route """
    return "OK"


@app.get("/identify/{creator}")
async def get_song_from_creator(creator: str):
    """ Identify a song based on creator name """
    print(f"Received song ID request for {creator}")
    start_time = datetime.utcnow().timestamp()
    created_file = get_stream_from_creator(creator)
    formatted_file = convert_mp4_to_mp3(created_file)

    # Recognize with shazam
    shazam = Shazam()
    shazam_song = await shazam.recognize_song(formatted_file)

    # Recognize with Audd
    audd_out = audd_recognize_song(formatted_file)
    audd_result = AuddResponse(**audd_out)

    audd_song = {}
    if audd_result.result is not None:
        audd_song = {
            "title": audd_result.result.get('title', None),
            "artist": audd_result.result.get('artist', None),
            "link": audd_result.result.get('song_link', None)
        }
    else:
        audd_song = {
            "title": None,
            "artist": None,
            "link": None
        }

    # Recognize with ACR
    acr_result = acr_identify(formatted_file)

    print(json.dumps(acr_result, indent=4, sort_keys=True))

    acr_song = {
        "title": None,
        "artist": None,
        "link": None
    }
    if acr_result is not None and acr_result.get('result_type', 1) == 0:
        track = acr_result.get('metadata').get('music')[0]

        if track is not None:
            acr_song = {
                "title": track.get('title'),
                "artist": track.get('artists')[0].get('name'),
                # "link": external_metadata.get(external_platform).get('vid')
                "link": ""
            }

    # Cleanup
    os.remove(created_file)
    os.remove(formatted_file)

    end_time = datetime.utcnow().timestamp()

    print(f"Handled song id in {end_time - start_time}s")

    return {
        "acr": acr_song,
        "audd": audd_song,
        "shazam": shazam_song
    }
