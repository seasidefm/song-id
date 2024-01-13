from shazamio import Shazam

from .BaseMatcher import BaseMatcher


class ShazamMatcher(BaseMatcher):
    """
    The base class for any audio sampling sources
    """

    async def match(self, sample_file: str) -> dict:
        shazam_client = Shazam(language="en-US", endpoint_country="US")

        return await shazam_client.recognize_song(sample_file)
