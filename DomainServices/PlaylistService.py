
# load modules
from cogs.Playlist import Playlist
from typing import Dict, List
from Domains.Song import Song, SongList
from urllib import request
from lxml import html


# definition
class PlaylistService:
    # 特定のプレイリストに関するサービス

    def add(self, keyword: str, url: str):
        pass
    # キーワードに一致するプレイリストを検索して、そこに曲を追加する

    # キーワードに一致するプレイリストを検索する
    def search(self, keyword: str) -> Playlist:
        pass


class PlaylistListService:
    # 全てのプレイリストに関するサービス

    # 新規の空のプレイリストを作成する
    def createEmpty(self):
        # Playlistを生成するために必要な要素は？
        # 主キー　→　他のプレイリストを全てロードしてナンバリングしないといけない。
        pass

    # 既存の空のプレイリストを削除する
    def deleteEmpty(self):
        pass

    # 既存のプレイリストを削除する
    def delete(self):
        # 空の場合はdeleteemptyを呼び出す。
        self.deleteEmpty()

    # 管理プレイリスト一覧を返す
    def show(self):
        pass

    # 全プレイリストのDLリンクを返す
    def download(self):
        pass
