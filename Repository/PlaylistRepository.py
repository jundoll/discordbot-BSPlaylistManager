
# load modules
from abc import ABCMeta, abstractmethod
from Domain.Playlist import Playlist,  PlaylistTitle


# definition
class IPlaylistRepository(metaclass=ABCMeta):

    # タイトルからプレイリストを読み込む
    @abstractmethod
    def findPlaylistByTitle(self, playlistTitle: PlaylistTitle) -> Playlist:
        pass

    # 指定のプレイリストを保存する
    @abstractmethod
    def save(self, playlist: Playlist):
        pass

    # 空のプレイリストを新規作成する
    @abstractmethod
    def create(self, playlist: Playlist):
        pass

    # 指定のプレイリストを削除する
    @abstractmethod
    def delete(self, playlistTitle: PlaylistTitle):
        pass

    # 指定のプレイリストのダウンロードURLを取得する
    @abstractmethod
    def getDownloadUrl(self, playlistTitle: PlaylistTitle) -> str:
        pass
