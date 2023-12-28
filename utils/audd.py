import requests
import os


async def audd_recognize_song(filename: str):
    try:
        data = {
            'api_token': os.getenv("AUDD_KEY"),
            'return': 'apple_music,spotify',
        }
        files = {
            'file': open(filename, 'rb'),
        }

        result = requests.post('https://api.audd.io/', data=data, files=files)
        print(result.content)
        return result.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Could not get audd.io source"}
