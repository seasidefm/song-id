class BaseMatcher:
    """
    The base class for any audio sampling sources
    """

    async def match(self, sample_file: str) -> dict:
        raise NotImplementedError("match() must be implemented by subclass")
