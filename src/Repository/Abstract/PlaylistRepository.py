
# load modules
from abc import ABCMeta, abstractmethod
from typing import List, Union
from src.Domain.Playlist import Playlist, PlaylistID, PlaylistKeyword, SearchKeyword
from src.Domain.Song import SongID


# definition
class IPlaylistRepository(metaclass=ABCMeta):

    # プレイリストを新規登録する
    @abstractmethod
    def insertPlaylist(self, playlist: Playlist):
        pass

    # プレイリストIDに対応するプレイリストの削除フラグをオンにする
    @abstractmethod
    def deletePlaylist(self, playlistID: PlaylistID):
        pass

    # プレイリストIDに対応するプレイリストの削除フラグをオフにする
    @abstractmethod
    def restorePlaylist(self, playlistID: PlaylistID):
        pass

    # プレイリストIDからプレイリストを読み込む
    @abstractmethod
    def findByID(self, playlistID: PlaylistID) -> Union[Playlist, None]:
        pass

    # キーワードからプレイリストを読み込む
    @abstractmethod
    def findByKeyword(self, playlistKeyword: PlaylistKeyword) -> Union[Playlist, None]:
        pass

    # キーワードからプレイリストIDを読み込む
    @abstractmethod
    def findIDByKeyword(self, playlistKeyword: PlaylistKeyword, isDeleted: bool = False) -> Union[PlaylistID, None]:
        pass

    # プレイリスト情報を更新する
    @abstractmethod
    def update(self, playlist: Playlist):
        pass

    # プレイリストへ曲を新規登録または更新する
    @abstractmethod
    def insertSong(self, playlistID: PlaylistID, songID: SongID):
        pass

    # プレイリストから曲を削除する
    @abstractmethod
    def deleteSong(self, playlistID: PlaylistID, songID: SongID):
        pass

    # 検索キーワードに対応する全てのプレイリストを読み込む
    @abstractmethod
    def fuzzyFindByKeyword(self, searchKeyword: SearchKeyword) -> Union[List[Playlist], None]:
        pass
