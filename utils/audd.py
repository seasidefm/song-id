import requests
import os


async def audd_recognize_song(filename: str):
    data = {
        'api_token': os.getenv("AUDD_KEY"),
        'return': 'apple_music,spotify',
    }
    files = {
        'file': open(filename, 'rb'),
    }

    result = requests.post('https://api.audd.io/', data=data, files=files)
    return result.json()
