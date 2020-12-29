
# load modules
from Domain.Song import Song
import os
from dataclasses import dataclass
from typing import List


# init settings
dl_path = os.environ['BS_PLAYLIST_DL_PATH']


# definition
@dataclass(frozen=True)
class PlaylistId:

    ID: str

    def __post_init__(self):

        # type check
        if not isinstance(self.ID, str):
            raise Exception

        # empty check
        if len(self.ID) == 0:
            raise Exception


@dataclass
class PlaylistFileName:

    playlistFileName: str

    def __post_init__(self):

        # type check
        if not isinstance(self.playlistFileName, str):
            raise Exception

        # empty check
        if len(self.playlistFileName) == 0:
            raise Exception

        # ファイル名に使えない記号などをはじく必要あり


@dataclass
class PlaylistTitle:

    playlistTitle: str
    # dropbox格納時に.jsonを付ける

    def __post_init__(self):

        # type check
        if not isinstance(self.playlistTitle, str):
            raise Exception

        # empty check
        if len(self.playlistTitle) == 0:
            raise Exception("タイトルは１文字以上で指定してね！")


@dataclass
class PlaylistInfo:

    playlistId: PlaylistId
    playlistFileName: PlaylistFileName
    playlistTitle: PlaylistTitle

    def __post_init__(self):

        # type check
        if not isinstance(self.playlistId, PlaylistId):
            raise Exception
        if not isinstance(self.playlistFileName, PlaylistFileName):
            raise Exception
        if not isinstance(self.playlistTitle, PlaylistTitle):
            raise Exception


@dataclass
class PlaylistAuthor:

    playlistAuthor: str
    # サーバ名からとってくるのもあり

    def __post_init__(self):

        # type check
        if not isinstance(self.playlistAuthor, str):
            raise Exception


@dataclass
class PlaylistDescription:

    playlistDescription: str

    def __post_init__(self):

        # type check
        if not isinstance(self.playlistDescription, str):
            raise Exception


@dataclass
class ImageBase64:

    image: str
    # 指定画像にプレイリスト名を埋めるとかありかも

    def __post_init__(self):

        # type check
        if not isinstance(self.image, str):
            raise Exception


@dataclass
class Playlist:

    playlistInfo: PlaylistInfo
    playlistTitle: PlaylistTitle
    playlistAuthor: PlaylistAuthor
    playlistDescription: PlaylistDescription
    image: ImageBase64
    songs: List[Song]

    def __post_init__(self):

        # type check
        if not isinstance(self.playlistInfo, PlaylistInfo):
            raise Exception
        if not isinstance(self.playlistTitle, PlaylistTitle):
            raise Exception
        if not isinstance(self.playlistAuthor, PlaylistAuthor):
            raise Exception
        if not isinstance(self.playlistDescription, PlaylistDescription):
            raise Exception
        if not isinstance(self.image, ImageBase64):
            raise Exception
        if not isinstance(self.songs, list):
            raise Exception
