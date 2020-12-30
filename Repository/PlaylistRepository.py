
# load modules
from abc import ABCMeta, abstractmethod
from typing import List, Union
from Domain.Playlist import Playlist, PlaylistInfo,  PlaylistTitle


# definition
class IPlaylistRepository(metaclass=ABCMeta):

    # ---------------------

    # タイトルからプレイリスト情報を読み込む
    @abstractmethod
    def readInfo(self, playlistTitle: PlaylistTitle) -> Union[PlaylistInfo, None]:
        pass

    # タイトルからプレイリスト情報一覧を読み込む
    @abstractmethod
    def readInfoList(self, playlistTitle: PlaylistTitle) -> Union[List[PlaylistInfo], None]:
        pass

    # ---------------------

    # プレイリスト情報を登録する
    @abstractmethod
    def registerInfo(self, playlistInfo: PlaylistInfo):
        pass

    # タイトルからプレイリスト情報を抹消する
    @abstractmethod
    def unregisterInfo(self, playlistTitle: PlaylistTitle):
        pass

    # ---------------------

    # タイトルからプレイリストを読み込む
    @abstractmethod
    def readPlaylist(self, playlistTitle: PlaylistTitle) -> Union[Playlist, None]:
        pass

    # ---------------------

    # プレイリストを保存する
    @abstractmethod
    def savePlaylist(self, playlist: Playlist):
        pass

    # プレイリストを削除する
    @abstractmethod
    def deletePlaylist(self, playlistTitle: PlaylistTitle):
        pass

    # ---------------------

    # タイトルからプレイリストのダウンロードURLを取得する
    @abstractmethod
    def getDownloadUrlByTitle(self, playlistTitle: PlaylistTitle) -> Union[str, None]:
        pass
