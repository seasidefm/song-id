from datetime import datetime
from os import getenv

from streamlink import Streamlink

from sampling.AudioSampler import AudioSampler


class StreamlinkSource(AudioSampler):
    def __init__(self, url: str, sample_duration: int):
        super().__init__(sample_duration)

        self.url = url
        self.session = None
        self.file_name = f'/tmp/{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.mp4'

    def prepare(self):
        stream_link = Streamlink()
        stream_link.set_option('twitch-low-latency', True)
        stream_link.set_option('twitch-disable-ads', True)
        stream_link.set_option('twitch-api-header', getenv('WATCH_TOKEN'))

        # General Settings / Stream Settings
        stream_link.set_option('hls-duration', 4)
        stream_link.set_option('ffmpeg-audio-transcode', 'aac')
        stream_link.set_option('retry-open', 4)
        stream_link.set_option('output', self.file_name)

        stream_link.set_option('hls-duration', self.sample_duration)

        stream_link.load_builtin_plugins()

        self.session = stream_link

    def get_sample(self) -> str:
        streams = self.session.streams(self.url)

        # read to a file
        with open(self.file_name, 'wb') as f:
            with streams.get('best').open() as stream:
                while True:
                    data = stream.read(1024)
                    if not data:
                        break
                    f.write(data)

        return self.file_name
