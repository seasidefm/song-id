import asyncio

from matcher.ShazamMatcher import ShazamMatcher


class Matcher:
    """
    The base class for any audio sampling sources
    """

    def __init__(self):
        self.shazam = ShazamMatcher()

    async def match(self, sample_file: str) -> dict:
        matches = await asyncio.gather(*[self.shazam.match(sample_file)])

        return {"shazam": matches[0]}
