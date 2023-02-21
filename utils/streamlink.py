""" Streamlink related utils """
from functools import partial
from os import getenv, replace, remove, path, rename
from datetime import datetime, timedelta
from subprocess import Popen, PIPE, STDOUT
from time import sleep

from streamlink import Streamlink, stream


def ceil_dt(dt, delta):
    return dt + (datetime.min - dt) % delta


def get_file_timestamp():
    return ceil_dt(datetime.now(), timedelta(seconds=10)).strftime('%H_%M_%S')


def get_new_file_name(filename: str):
    timestamp = get_file_timestamp()
    return f"{getenv('TMP_DIR')}/{filename}.mp4"


def get_stream_from_creator(creator: str) -> str:
    """ Take a creator handle and attempt to get the stream bytes """
    print("Creating streamlink session")
    session = Streamlink()

    # General Settings / Stream Settings
    # session.set_option('hls-duration', 4)
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
    with best_stream.open() as stream_bytes:
        loop_count = 0
        test_count = 0

        # Prepare files
        current = get_new_file_name("current")
        previous = get_new_file_name("previous")

        file = open(current, 'wb')
        for byte_content in iter(partial(stream_bytes.read, 5_000_000), b""):
            if test_count >= 5:
                break

            print("got bytes from stream")
            file.write(byte_content)

            if loop_count > 4:
                # Close "current"
                file.close()

                if path.exists(previous):
                    # mv <src> <destination>
                    replace(current, previous)
                else:
                    rename(current, previous)

                file = open(current, "wb")

                test_count += 1
            else:
                sleep(5)
                loop_count += 1

        file.close()

    return get_new_file_name("previous.mp4")
