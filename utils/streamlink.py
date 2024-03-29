""" Streamlink related utils """
import logging
import os
from os import getenv
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

from streamlink import Streamlink
from streamlink.stream import stream


class StreamFetcher:
    """Streamlink wrapper class"""

    def __init__(self):
        self.session = None
        self.logger = logging.getLogger("song-id")
        self.streamlink_bin = os.getenv("STREAMLINK_BIN")

    def init_session(self):
        """Create a new streamlink session"""
        self.session = Streamlink()

        # Twitch options
        self.session.set_option("twitch-low-latency", True)
        self.session.set_option("twitch-disable-ads", True)
        self.session.set_option("twitch-api-header", getenv("WATCH_HEADER"))

        # General Settings / Stream Settings
        self.session.set_option("hls-duration", self)
        self.session.set_option("ffmpeg-audio-transcode", "aac")
        self.session.set_option("retry-open", 4)
        self.session.set_option(
            "output", f'{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4'
        )

        # Load streams here
        self.session.load_builtin_plugins()

    def get_best_stream(self, creator: str) -> stream.Stream:
        """Take a creator handle and attempt to get the stream bytes"""
        streams = self.session.streams(f"https://wwww.twitch.tv/{creator}")

        return streams.get("best")

    def stream_via_cli(self, creator: str, filename: str):
        """Stream via CLI"""

        command = [
            self.streamlink_bin,
            f'--twitch-api-header=Authorization=OAuth {getenv("WATCH_HEADER")}',
            "--twitch-disable-ads",
            "--twitch-low-latency",
            "--hls-duration",
            "00:05",
            "--ffmpeg-audio-transcode",
            '"aac"',
            "--retry-open",
            "6",
            "--stream-segment-threads",
            "3",
            "--output",
            filename,
            f"https://www.twitch.tv/{creator}",
            "best",
        ]

        self.logger.debug(command)

        with Popen(command, stdout=PIPE, stderr=STDOUT) as proc:
            for line in proc.stdout:
                self.logger.debug(line.decode("utf-8").strip())

            code = proc.wait()
            if code != 0:
                self.logger.error(f"Received code {code} from stream watcher thread")


def get_stream_from_creator(creator: str) -> str:
    """Take a creator handle and attempt to get the stream bytes"""
    print("Creating streamlink session")
    # session = Streamlink()
    #
    # # General Settings / Stream Settings
    # session.set_option('hls-duration', 8)
    # session.set_option('ffmpeg-audio-transcode', 'aac')
    # session.set_option('retry-open', 10)
    #
    # # Twitch options
    # session.set_option('twitch-low-latency', True)
    # session.set_option('twitch-disable-ads', True)
    # session.set_option('twitch-api-header', getenv('WATCH_HEADER'))
    #
    # # Load streams here
    # session.load_builtin_plugins()
    # streams = session.streams(f"https://wwww.twitch.tv/{creator}")
    # #
    # best_stream: stream.Stream = streams.get('best')
    # #
    # print("Streaming to disk...")
    # # stream_bytes = best_stream.open()
    #

    timestamp = datetime.utcnow().timestamp()
    filename = f"{getenv('TMP_DIR')}/{timestamp}-{creator}.mp4"
    command = [
        os.getenv("STREAMLINK_BIN"),
        f'--twitch-api-header=Authorization=OAuth {getenv("WATCH_HEADER")}',
        "--twitch-disable-ads",
        "--twitch-low-latency",
        "--hls-duration",
        "00:05",
        "--ffmpeg-audio-transcode",
        '"aac"',
        "--retry-open",
        "4",
        "--output",
        filename,
        f"https://www.twitch.tv/{creator}",
        "best",
    ]

    with Popen(command, stdout=PIPE, stderr=STDOUT) as proc:
        out = proc.stdout.read()

        for line in out.splitlines():
            print(">>> " + str(line))

    print("Done streaming!")
    return filename
