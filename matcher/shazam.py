"""
Module for interactions with the Shazam API
"""

from shazamio import Shazam as ShazamIO


class Shazam:
    """
    Wrapper class for interacting with ShazamIO library, and ultimately the Shazam service
    """

    def __init__(self):
        self.shazam = ShazamIO(language="en-US")

    async def identify(self, file_name: str):
        """
        Attempt to identify song using Shazam service
        :param file_name:
        :return:
        """
        return await self.shazam.recognize_song(file_name)

    @staticmethod
    def from_env():
        """
        API unifier function, just return a new instance of this class
        :return:
        """
        return Shazam()
