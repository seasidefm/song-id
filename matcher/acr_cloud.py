"""
Module for interacting with ACR Cloud
"""

import base64
import hashlib
import hmac
import os
import time

import requests


class AcrCloud:
    """
    Acr Cloud interaction service
    """

    def __init__(self, access_key: str, access_secret: str, access_host: str):
        self.access_key = access_key
        self.access_secret = access_secret
        self.access_host = access_host

    async def identify(self, filename: str):
        """
        Attempt to identify a song via ACR Cloud given a filename
        """

        requrl = f"https://{self.access_host}/v1/identify"

        http_method = "POST"
        http_uri = "/v1/identify"
        # default is "fingerprint", it's for recognizing fingerprint,
        # if you want to identify audio, please change data_type="audio"
        data_type = "audio"
        signature_version = "1"
        timestamp = time.time()

        string_to_sign = http_method + \
            "\n" + http_uri + \
            "\n" + self.access_key + \
            "\n" + data_type + \
            "\n" + signature_version \
            + "\n" + str(timestamp)

        sign = base64.b64encode(hmac.new(self.access_secret.encode('ascii'), string_to_sign.encode('ascii'),
                                         digestmod=hashlib.sha1).digest()).decode('ascii')

        with open(filename, "rb") as file:
            sample_bytes = os.path.getsize(filename)

            files = [
                ('song_id', ('test.mp3', file, 'audio/mpeg'))
            ]
            data = {'access_key': self.access_key,
                    'sample_bytes': sample_bytes,
                    'timestamp': str(timestamp),
                    'signature': sign,
                    'data_type': data_type,
                    "signature_version": signature_version}

            res = requests.post(requrl, files=files, data=data)
            res.encoding = "utf-8"

            data = res.json()

            if data.get('result_type') != 0:
                return None

            return data

    @staticmethod
    def from_env():
        """ Get a new AcrCloud instance from ENV """
        return AcrCloud(
            os.getenv('ACR_ACCESS_KEY'),
            os.getenv('ACR_ACCESS_SECRET'),
            os.getenv('ACR_ACCESS_HOST'),
        )
