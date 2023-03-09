""" Streamlink related utils """

from os import getenv
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

from streamlink import Streamlink
from streamlink.stream import stream


class StreamFetcher:
    """ Streamlink wrapper class """
    def __init__(self):
        self.session = None

    def init_session(self):
        """ Create a new streamlink session """
        self.session = Streamlink()

        # General Settings / Stream Settings
        self.session.set_option('hls-duration', 5)
        self.session.set_option('ffmpeg-audio-transcode', 'aac')
        self.session.set_option('retry-open', 10)

        # Twitch options
        self.session.set_option('twitch-low-latency', True)
        self.session.set_option('twitch-disable-ads', True)
        self.session.set_option('twitch-api-header', getenv('WATCH_TOKEN'))

        # Load streams here
        self.session.load_builtin_plugins()

    def get_best_stream(self, creator: str) -> stream.Stream:
        """ Take a creator handle and attempt to get the stream bytes """
        streams = self.session.streams(f"https://wwww.twitch.tv/{creator}")

        return streams.get('best')


def get_stream_from_creator(creator: str) -> str:
    """ Take a creator handle and attempt to get the stream bytes """
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
    # session.set_option('twitch-api-header', getenv('WATCH_TOKEN'))
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
        'streamlink',
        f'--twitch-api-header=Authorization=OAuth {getenv("WATCH_TOKEN")}',
        "--twitch-disable-ads",
        "--twitch-low-latency",
        # "--hls-duration",
        # '00:08',
        "--ffmpeg-audio-transcode",
        '"aac"',
        "--retry-open",
        "4",
        "--output",
        filename,
        f"https://www.twitch.tv/{creator}",
        'best'
    ]

    with Popen(command, stdout=PIPE, stderr=STDOUT) as proc:
        out = proc.stdout.read()

        for line in out.splitlines():
            print(">>> " + str(line))


    print("Done streaming!")
    return filename
