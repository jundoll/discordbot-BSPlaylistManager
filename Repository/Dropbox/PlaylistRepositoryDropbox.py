
# load modules
from typing import List, Union
from Domain.Playlist import Playlist, PlaylistInfo, PlaylistTitle
from Repository.Dropbox.Dropbox import Dropbox
from Repository.PlaylistRepository import IPlaylistRepository


# definition
class PlaylistRepositoryDropbox(IPlaylistRepository):

    def __init__(self):
        self.dropbox = Dropbox()

    # ---------------------

    # タイトルからプレイリスト情報を読み込む
    def readInfo(self, playlistTitle: PlaylistTitle) -> Union[PlaylistInfo, None]:

        # タイトルからプレイリスト情報を読み込む
        playlistInfo = self.dropbox.readInfoByTitle(playlistTitle)
        return playlistInfo

    # プレイリスト情報一覧を読み込む
    def readInfoList(self) -> Union[List[PlaylistInfo], None]:

        # プレイリスト情報一覧を読み込む
        playlistInfoList = self.dropbox.readInfoListByTitle()
        return playlistInfoList

    # ---------------------

    # プレイリスト情報を登録する
    def registerInfo(self, playlistInfo: PlaylistInfo):

        # プレイリスト情報一覧を読み込む
        playlistInfoList = self.readInfoList()
        if playlistInfoList is None:
            playlistInfoList = []

        # 重複チェック
        if len(playlistInfoList) > 0:
            if playlistInfo.playlistTitle in [info.playlistTitle for info in playlistInfoList]:
                raise Exception("既に存在するタイトルだよ！違う名前に変えてね！")

        # プレイリスト情報をプレイリスト情報一覧に追加する
        playlistInfoList.append(playlistInfo)

        # プレイリスト情報一覧を保存する
        self.dropbox.saveInfoList(playlistInfoList)

    # タイトルからプレイリスト情報を抹消する
    def unregisterInfo(self, playlistTitle: PlaylistTitle):

        # プレイリスト情報一覧を読み込む
        playlistInfoList = self.readInfoList()
        if playlistInfoList is None:
            playlistInfoList = []

        # タイトルからプレイリスト情報を取得する
        playlistInfo = self.readInfo(playlistTitle)
        if playlistInfo is None:
            return

        # プレイリスト情報をプレイリスト情報一覧から削除する
        playlistInfoList.remove(playlistInfo)

        # プレイリスト情報一覧を保存する
        self.dropbox.saveInfoList(playlistInfoList)

    # ---------------------

    # タイトルからプレイリストを読み込む
    def readPlaylist(self, playlistTitle: PlaylistTitle) -> Union[Playlist, None]:

        # タイトルからプレイリスト情報を検索する
        playlistInfo = self.readInfo(playlistTitle)
        if playlistInfo is None:
            return

        # プレイリスト情報のファイル名に基づきファイルを読み込む
        playlist = self.dropbox.readPlaylist(playlistInfo)
        return playlist

    # ---------------------

    # プレイリストを保存する
    def savePlaylist(self, playlist: Playlist):

        # プレイリストを保存する
        self.dropbox.savePlaylist(playlist)

    # タイトルからプレイリストを削除する
    def deletePlaylist(self, playlistTitle: PlaylistTitle):

        # タイトルからプレイリストを削除する
        self.dropbox.deletePlaylist(playlistTitle)

    # ---------------------

    # タイトルからプレイリストのダウンロードURLを取得する
    def getDownloadUrl(self, playlistTitle: PlaylistTitle) -> Union[str, None]:

        # タイトルからプレイリストのダウンロードURLを取得する
        url = self.dropbox.getSharedLink(playlistTitle)
        return url
