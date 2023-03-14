"""
Module for interactions with Audd.io service
"""

import os

import requests


class Auddio:
    """
    Wrapper class for interacting with Audd.io service
    """
    def __init__(self, audd_key: str):
        self.audd_key = audd_key

    async def identify(self, filename: str):
        """
        Attempt to identify song from given file using Audd.io

        :param filename:
        :return:
        """
        with open(filename, 'rb') as file:
            data = {
                'api_token': self.audd_key,
                'return': 'apple_music,spotify',
            }
            files = {
                'file': file,
            }

            result = requests.post('https://api.audd.io/', data=data, files=files)
            return result.json()

    @staticmethod
    def from_env():
        """
        Pull required key(s) from env and return instance.

        Throws if key(s) not found
        :return:
        """
        key = os.getenv('AUDD_KEY')

        if key is None:
            raise EnvironmentError("Cannot find AUDD_KEY in environment!")

        return Auddio(key)
