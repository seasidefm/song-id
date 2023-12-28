from typing import List
from datetime import datetime


class Artwork:
    width: int
    height: int
    url: str
    bg_color: str
    text_color1: str
    text_color2: str
    text_color3: str
    text_color4: str

    def __init__(self, width: int, height: int, url: str, bg_color: str, text_color1: str, text_color2: str, text_color3: str, text_color4: str) -> None:
        self.width = width
        self.height = height
        self.url = url
        self.bg_color = bg_color
        self.text_color1 = text_color1
        self.text_color2 = text_color2
        self.text_color3 = text_color3
        self.text_color4 = text_color4


class PlayParams:
    id: int
    kind: str

    def __init__(self, id: int, kind: str) -> None:
        self.id = id
        self.kind = kind


class Preview:
    url: str

    def __init__(self, url: str) -> None:
        self.url = url


class AppleMusic:
    previews: List[Preview]
    artwork: Artwork
    artist_name: str
    url: str
    disc_number: int
    genre_names: List[str]
    duration_in_millis: int
    release_date: datetime
    name: str
    isrc: str
    album_name: str
    play_params: PlayParams
    track_number: int
    composer_name: str

    def __init__(self, previews: List[Preview], artwork: Artwork, artist_name: str, url: str, disc_number: int, genre_names: List[str], duration_in_millis: int, release_date: datetime, name: str, isrc: str, album_name: str, play_params: PlayParams, track_number: int, composer_name: str) -> None:
        self.previews = previews
        self.artwork = artwork
        self.artist_name = artist_name
        self.url = url
        self.disc_number = disc_number
        self.genre_names = genre_names
        self.duration_in_millis = duration_in_millis
        self.release_date = release_date
        self.name = name
        self.isrc = isrc
        self.album_name = album_name
        self.play_params = play_params
        self.track_number = track_number
        self.composer_name = composer_name


class ExternalUrls:
    spotify: str

    def __init__(self, spotify: str) -> None:
        self.spotify = spotify


class Artist:
    name: str
    id: str
    uri: str
    href: str
    external_urls: ExternalUrls

    def __init__(self, name: str, id: str, uri: str, href: str, external_urls: ExternalUrls) -> None:
        self.name = name
        self.id = id
        self.uri = uri
        self.href = href
        self.external_urls = external_urls


class Image:
    height: int
    width: int
    url: str

    def __init__(self, height: int, width: int, url: str) -> None:
        self.height = height
        self.width = width
        self.url = url


class Album:
    name: str
    artists: List[Artist]
    album_group: str
    album_type: str
    id: str
    uri: str
    available_markets: List[str]
    href: str
    images: List[Image]
    external_urls: ExternalUrls
    release_date: datetime
    release_date_precision: str

    def __init__(self, name: str, artists: List[Artist], album_group: str, album_type: str, id: str, uri: str, available_markets: List[str], href: str, images: List[Image], external_urls: ExternalUrls, release_date: datetime, release_date_precision: str) -> None:
        self.name = name
        self.artists = artists
        self.album_group = album_group
        self.album_type = album_type
        self.id = id
        self.uri = uri
        self.available_markets = available_markets
        self.href = href
        self.images = images
        self.external_urls = external_urls
        self.release_date = release_date
        self.release_date_precision = release_date_precision


class ExternalIDS:
    isrc: str

    def __init__(self, isrc: str) -> None:
        self.isrc = isrc


class Spotify:
    album: Album
    external_ids: ExternalIDS
    popularity: int
    is_playable: None
    linked_from: None
    artists: List[Artist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_urls: ExternalUrls
    href: str
    id: str
    name: str
    preview_url: str
    track_number: int
    uri: str

    def __init__(self, album: Album, external_ids: ExternalIDS, popularity: int, is_playable: None, linked_from: None, artists: List[Artist], available_markets: List[str], disc_number: int, duration_ms: int, explicit: bool, external_urls: ExternalUrls, href: str, id: str, name: str, preview_url: str, track_number: int, uri: str) -> None:
        self.album = album
        self.external_ids = external_ids
        self.popularity = popularity
        self.is_playable = is_playable
        self.linked_from = linked_from
        self.artists = artists
        self.available_markets = available_markets
        self.disc_number = disc_number
        self.duration_ms = duration_ms
        self.explicit = explicit
        self.external_urls = external_urls
        self.href = href
        self.id = id
        self.name = name
        self.preview_url = preview_url
        self.track_number = track_number
        self.uri = uri


class Result:
    artist: str
    title: str
    album: str
    release_date: datetime
    label: str
    timecode: str
    song_link: str
    apple_music: AppleMusic
    spotify: Spotify

    def __init__(self, artist: str, title: str, album: str, release_date: datetime, label: str, timecode: str, song_link: str, apple_music: AppleMusic, spotify: Spotify) -> None:
        self.artist = artist
        self.title = title
        self.album = album
        self.release_date = release_date
        self.label = label
        self.timecode = timecode
        self.song_link = song_link
        self.apple_music = apple_music
        self.spotify = spotify


class AuddResponse:
    status: str
    result: Result

    def __init__(self, status: str, result: Result) -> None:
        self.status = status
        self.result = result