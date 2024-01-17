class VideoProcessor:
    """
    The base class for any audio sampling sources
    """

    async def process(self, input_file: str, output_file: str) -> str:
        raise NotImplementedError("process() must be implemented by subclass")
