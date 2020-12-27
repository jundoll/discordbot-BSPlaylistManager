
# load modules
from typing import List
from Domains.Song import SongList
import dataclasses
import os
from dataclasses import dataclass, field

# init settings
dl_path = os.environ['BS_PLAYLIST_DL_PATH']


# definition
@dataclass
class Image:

    image: str
    # 指定画像にプレイリスト名を埋めるとかありかも


@dataclass
class Playlist:

    key: str  # プレイリストを管理する主キー
    playlistFileName: str
    playlistTitle: str  # Playlist01 みたくナンバリング or 時刻
    playlistAuthor: str  # サーバ名？
    playlistDescription: str  # デフォルトは無し
    image: Image  # デフォルト画像を。
    songs:SongList=field(default=SongList())  # デフォルトは

    def __eq__(self, other) -> bool:
        return self.key == other.key


@dataclass
class PlaylistList():

    playlistList = List[Playlist]

    def append(self):
        pass

    def remove(self):
        pass
