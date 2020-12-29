
# load modules
from Application.Playlists.PlaylistApplicationService import PlaylistApplicationService
from Factory.SongFactory import ISongFactory
from Domain.Playlist import PlaylistTitle
import inject
from Repository.PlaylistRepository import IPlaylistRepository


# definition
class SongApplicationService:
    # 凝集度などの問題で分割が必要になったら分ける

    # instance fields
    songFactory: ISongFactory = inject.attr(ISongFactory)

    # post init
    def __post__init__(self):

        # type check
        if not isinstance(self.songFactory, ISongFactory):
            raise Exception

    # タイトルに一致するプレイリストを検索して、曲を追加する
    # urlがmapperだったらmapperの曲すべてを追加する（今後実装）
    def add(self, title: str, url: str):

        # type check
        if not isinstance(title, str):
            raise Exception
        if not isinstance(url, str):
            raise Exception

        # 対象プレイリストを検索する
        playlistApplicationService = PlaylistApplicationService()
        foundPlaylist = playlistApplicationService.find(title)

        # 対象プレイリストに曲を追加する
        # 重複時のメッセージをつける場合はこの辺をいじる
        song = self.songFactory.create(url)
        foundPlaylist.songs.append(song)

        # 対象プレイリストの重複を削除する
        foundPlaylist.songs = list(set(foundPlaylist.songs))

        # プレイリストを更新する
        playlistApplicationService.save(foundPlaylist)

    # タイトルに一致するプレイリストを検索して、曲を削除する
    # mapper指定の場合、どこまで消すか？全部になるか...
    def delete(self, title: str, url: str):

        # type check
        if not isinstance(title, str):
            raise Exception
        if not isinstance(url, str):
            raise Exception

        # 対象プレイリストを検索する
        playlistApplicationService = PlaylistApplicationService()
        foundPlaylist = playlistApplicationService.find(title)

        # 対象プレイリストから曲を削除する
        song = self.songFactory.create(url)
        foundPlaylist.songs.remove(song)

        # プレイリストを更新する
        playlistApplicationService.save(foundPlaylist)
