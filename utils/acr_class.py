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
