from typing import Optional, List
from datetime import datetime


class Album:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class ExternalIDS:
    isrc: str
    upc: str

    def __init__(self, isrc: str, upc: str) -> None:
        self.isrc = isrc
        self.upc = upc


class Lang:
    name: str
    code: str

    def __init__(self, name: str, code: str) -> None:
        self.name = name
        self.code = code


class Artist:
    name: str
    langs: Optional[List[Lang]]

    def __init__(self, name: str, langs: Optional[List[Lang]]) -> None:
        self.name = name
        self.langs = langs


class Track:
    id: int
    name: str

    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name


class Deezer:
    artists: List[Artist]
    track: Track
    album: Album

    def __init__(self, artists: List[Artist], track: Track, album: Album) -> None:
        self.artists = artists
        self.track = track
        self.album = album


class Youtube:
    vid: str

    def __init__(self, vid: str) -> None:
        self.vid = vid


class ExternalMetadata:
    deezer: Deezer
    youtube: Youtube

    def __init__(self, deezer: Deezer, youtube: Youtube) -> None:
        self.deezer = deezer
        self.youtube = youtube


class Genre:
    name: str
    id: int

    def __init__(self, name: str, id: int) -> None:
        self.name = name
        self.id = id


class Music:
    external_metadata: ExternalMetadata
    label: str
    result_from: int
    acrid: str
    duration_ms: int
    db_begin_time_offset_ms: int
    db_end_time_offset_ms: int
    sample_begin_time_offset_ms: int
    sample_end_time_offset_ms: int
    play_offset_ms: int
    release_date: datetime
    genres: List[Genre]
    album: Album
    external_ids: ExternalIDS
    artists: List[Album]
    title: str
    score: int

    def __init__(self, external_metadata: ExternalMetadata, label: str, result_from: int, acrid: str, duration_ms: int, db_begin_time_offset_ms: int, db_end_time_offset_ms: int, sample_begin_time_offset_ms: int, sample_end_time_offset_ms: int, play_offset_ms: int, release_date: datetime, genres: List[Genre], album: Album, external_ids: ExternalIDS, artists: List[Album], title: str, score: int) -> None:
        self.external_metadata = external_metadata
        self.label = label
        self.result_from = result_from
        self.acrid = acrid
        self.duration_ms = duration_ms
        self.db_begin_time_offset_ms = db_begin_time_offset_ms
        self.db_end_time_offset_ms = db_end_time_offset_ms
        self.sample_begin_time_offset_ms = sample_begin_time_offset_ms
        self.sample_end_time_offset_ms = sample_end_time_offset_ms
        self.play_offset_ms = play_offset_ms
        self.release_date = release_date
        self.genres = genres
        self.album = album
        self.external_ids = external_ids
        self.artists = artists
        self.title = title
        self.score = score


class Metadata:
    timestamp_utc: datetime
    music: List[Music]

    def __init__(self, timestamp_utc: datetime, music: List[Music]) -> None:
        self.timestamp_utc = timestamp_utc
        self.music = music


class Status:
    code: int
    msg: str
    version: str

    def __init__(self, code: int, msg: str, version: str) -> None:
        self.code = code
        self.msg = msg
        self.version = version


class AcrResult:
    result_type: int
    metadata: Metadata
    cost_time: float
    status: Status

    def __init__(self, result_type: int, metadata: Metadata, cost_time: float, status: Status) -> None:
        self.result_type = result_type
        self.metadata = metadata
        self.cost_time = cost_time
        self.status = status

# external_metadata = metadata.get('music')[0].get('external_metadata')
# track = external_metadata.get('deezer').get('track')
# album = external_metadata.get('deezer').get('album')
# artists = external_metadata.get('deezer').get('artists')
# {
#     'result_type': 0, 'metadata': {'timestamp_utc': '2023-02-26 22:20:47', 'music': [{'album': {'name': 'Palmscapes'}, 'score': 100, 'release_date': '2021-06-04', 'artists': [{'name': 'Hotel Pools'}], 'external_ids': {'isrc': 'QZES62147290', 'upc': '196052847585'}, 'external_metadata': {'deezer': {'artists': [{'name': 'Hotel Pools'}], 'album': {'name': ''}, 'track': {'id': '1290221242', 'name': 'Oceanside'}}, 'spotify': {'artists': [{'name': 'Hotel Pools'}], 'album': {'name': 'Palmscapes'}, 'track': {'id': '0HcM1AiNLkjq5qW68siA1K', 'name': 'Oceanside'}}}, 'db_end_time_offset_ms': 188260, 'sample_begin_time_offset_ms': 0, 'sample_end_time_offset_ms': 9760, 'play_offset_ms': 188260, 'result_from': 1, 'label': 'Wild Nature / Stratford Ct.', 'acrid': 'ec0f48014632b53b2f9c64f662c257de', 'db_begin_time_offset_ms': 178620, 'duration_ms': 206260, 'title': 'Oceanside'}]}, 'cost_time': 0.53299999237061, 'status': {'msg': 'Success', 'version': '1.0', 'code': 0}}