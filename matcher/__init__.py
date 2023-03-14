"""
The main business logic class for the Song ID platform
"""

import asyncio
from typing import Union

from pydantic import BaseModel
from .acr_cloud import AcrCloud
from .auddio import Auddio
from .shazam import Shazam


class SongMatch(BaseModel):
    """The standardized result of a song match."""
    title: Union[str, None]
    artist: Union[str, None]
    link: Union[str, None]


class SongMatcher:
    """
    Unified song ID source class wrapper

    To avoid having to account for EVERY source in EVERY location an ID is needed, use this class :)
    """

    def __init__(self):
        self.acr_cloud = AcrCloud.from_env()
        self.auddio = Auddio.from_env()
        self.shazam = Shazam.from_env()

    async def identify_from_file(self, filename: str) -> SongMatch:
        """
        Pass a given file name to all selected Song ID services

        :param filename:
        :return:
        """
        acr_cloud, auddio, shazam = await asyncio.gather(*[
            self.acr_cloud.identify(filename),
            self.auddio.identify(filename),
            self.shazam.identify(filename)
        ])

        # TODO: Parse/handle response objects

        return SongMatch()
