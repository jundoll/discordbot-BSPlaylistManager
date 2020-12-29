
# load modules
from abc import ABCMeta, abstractmethod
from typing import Union

from Domain.Playlist import Playlist,  PlaylistId, PlaylistTitle


# definition
class IPlaylistRepository(ABCMeta):

    # タイトルからプレイリストを読み込む
    @abstractmethod
    def findPlaylistByTitle(self, playlistTitle: PlaylistTitle) -> Playlist:
        pass

    # 指定のプレイリストを保存する
    @abstractmethod
    def save(self, playlist: Playlist):
        pass

    @abstractmethod
    def create(self, playlist: Playlist):
        pass

    @abstractmethod
    def findPlaylistId(self, playlistId: PlaylistId) -> Union[Playlist, None]:
        pass
    # 存在したらそのプレイリスト情報を。存在しなければNoneを返す方が自然か。
