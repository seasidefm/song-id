""" Streamlink related utils """

from os import getenv
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT


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
    #
    # best_stream: stream.Stream = streams.get('best')
    #
    print("Streaming to disk...")
    # stream_bytes = best_stream.open()
    #

    timestamp = datetime.utcnow().timestamp()
    filename = f"{getenv('TMP_DIR')}/{timestamp}-{creator}.mp4"
    command = [
        'streamlink',
        f'--twitch-api-header=Authorization=OAuth {getenv("WATCH_TOKEN")}',
        "--twitch-disable-ads",
        "--twitch-low-latency",
        "--hls-duration",
        '00:08',
        "--ffmpeg-audio-transcode",
        '"aac"',
        "--retry-open",
        "4",
        "-r",
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
