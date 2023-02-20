from os import getenv
from streamlink import Streamlink, stream
from datetime import datetime


def get_stream_from_creator(creator: str) -> str:
    """ Take a creator handle and attempt to get the stream bytes """
    print("Creating streamlink session")
    session = Streamlink()

    # General Settings / Stream Settings
    session.set_option('hls-duration', 8)
    session.set_option('ffmpeg-audio-transcode', 'aac')
    session.set_option('retry-open', 10)

    # Twitch options
    session.set_option('twitch-low-latency', True)
    session.set_option('twitch-disable-ads', True)
    session.set_option('twitch-api-header', getenv('WATCH_TOKEN'))

    # Load streams here
    session.load_builtin_plugins()
    streams = session.streams(f"https://wwww.twitch.tv/{creator}")

    best_stream: stream.Stream = streams.get('best')

    print("Streaming to disk...")
    stream_bytes = best_stream.open()

    timestamp = datetime.utcnow().timestamp()
    filename = f"{getenv('TMP_DIR')}/{timestamp}-{creator}.mp4"
    with open(filename, "wb") as mp4_file:
        mp4_file.writelines(stream_bytes.readlines())
        mp4_file.close()

    print("Done streaming!")
    return filename
