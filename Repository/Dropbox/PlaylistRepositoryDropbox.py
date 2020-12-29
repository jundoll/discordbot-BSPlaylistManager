
# load modules
from importlib.abc import ExecutionLoader
from Repository.Dropbox.Dropbox import Dropbox
from typing import Union
from Repository.PlaylistRepository import IPlaylistRepository
from Domain.Playlist import Playlist, PlaylistId, PlaylistInfo, PlaylistTitle


# definition
class PlaylistRepositoryDropbox(IPlaylistRepository):

    def __init__(self):
        self.dropbox = Dropbox()

    # タイトルからプレイリストを読み込む
    def findPlaylistByTitle(self, playlistTitle: PlaylistTitle) -> Playlist:
        # タイトルからプレイリスト情報を検索する
        playlistInfo = self.dropbox.findInfoByTitle(playlistTitle)
        if playlistInfo is None:
            raise Exception("指定のプレイリストが見つからないよ！")
        else:
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
