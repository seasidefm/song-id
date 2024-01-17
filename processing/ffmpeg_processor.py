from ffmpeg.asyncio import ffmpeg

from processing.VideoProcessor import VideoProcessor


class FfmpegProcessor(VideoProcessor):
    async def process(self, input_file: str, output_file: str) -> str:
        await ffmpeg.FFmpeg().input(input_file).output(output_file).execute()

        return output_file
