
# load modules
from typing import Union
from Domain.Playlist import Playlist, PlaylistTitle
from Repository.Dropbox.Dropbox import Dropbox
from Repository.PlaylistRepository import IPlaylistRepository


# definition
class PlaylistRepositoryDropbox(IPlaylistRepository):

    def __init__(self):
        self.dropbox = Dropbox()

    # タイトルからプレイリストを読み込む
    def findPlaylistByTitle(self, playlistTitle: PlaylistTitle) -> Union[Playlist, None]:
        # タイトルからプレイリスト情報を検索する
        playlistInfo = self.dropbox.findInfoByTitle(playlistTitle)
        if playlistInfo is not None:
            # プレイリスト情報のファイル名に基づきファイルを読み込む
            # （１．ファイル名からファイルパスを取得する）
            # （２．ファイルパスに基づき、json ファイルを読み込む）
            # （３．json 形式のプレイリストを Playlist インスタンスに変換する）
            playlist = self.dropbox.readPlaylistJsonByFileName(
                playlistInfo.playlistFileName)
            return playlist

    # 指定のプレイリストを保存する
    def save(self, playlist: Playlist):
        # プレイリストを保存する
        self.dropbox.savePlaylistJson(playlist)

    # 空のプレイリストを新規作成する
    def create(self, playlist: Playlist):
        # プレイリスト情報を情報一覧に追加する
        self.dropbox.registerInfo(playlist.playlistInfo)
        # プレイリストを保存する
        self.dropbox.savePlaylistJson(playlist)

    # 指定のプレイリストを削除する
    def delete(self, playlistTitle: PlaylistTitle):
        # タイトルからプレイリスト情報を検索する
        playlistInfo = self.dropbox.findInfoByTitle(playlistTitle)
        if playlistInfo is None:
            raise Exception("指定のプレイリストが見つからないよ！")
        else:
            # プレイリスト情報を情報一覧から削除する
            self.dropbox.unregisterInfo(playlistInfo)
            # プレイリストを削除する
            self.dropbox.deletePlaylist(playlistInfo)

    # 指定のプレイリストのダウンロードURLを取得する
    def getDownloadUrl(self, playlistTitle: PlaylistTitle) -> str:
        url = self.dropbox.getSharedLink(playlistTitle)
        return url
