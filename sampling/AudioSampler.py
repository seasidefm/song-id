class AudioSampler:
    """
    The base class for any audio sampling sources
    """

    def __init__(self, sample_duration: int = 7):
        self.sample_duration = sample_duration

    def prepare(self):
        raise NotImplementedError("prepare() must be implemented by subclass")

    def get_sample(self) -> str:
        raise NotImplementedError("get_sample() must be implemented by subclass")
