
# load modules
import inject
from Domain.Playlist import PlaylistTitle
from Factory.SongFactory import ISongFactory
from Application.PlaylistApplicationService import PlaylistApplicationService


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

    # ---------------------

    # タイトルに一致するプレイリストを検索して、曲を追加する
    # urlがmapperだったらmapperの曲すべてを追加する（今後実装）
    def add(self, title: str, url: str):

        # type check
        if not isinstance(title, str):
            raise Exception
        if not isinstance(url, str):
            raise Exception

        # タイトルに一致するプレイリストを検索する
        playlistApplicationService = PlaylistApplicationService()
        playlistTitle = PlaylistTitle(title)
        playlist = playlistApplicationService.find(playlistTitle)

        # 対象プレイリストに曲を追加する
        song = self.songFactory.create(url)
        playlist.songs.append(song)

        # 対象プレイリストの重複を削除する
        playlist.songs = list(set(playlist.songs))

        # プレイリストを更新する
        playlistApplicationService.save(playlist)

    # ---------------------

    # タイトルに一致するプレイリストを検索して、曲を削除する
    # mapper指定の場合、どこまで消すか？全部になるか...
    def delete(self, title: str, url: str):

        # type check
        if not isinstance(title, str):
            raise Exception
        if not isinstance(url, str):
            raise Exception

        # タイトルに一致するプレイリストを検索する
        playlistApplicationService = PlaylistApplicationService()
        playlist = playlistApplicationService.find(title)

        # 対象プレイリストに曲を追加する
        song = self.songFactory.create(url)
        try:
            playlist.songs.remove(song)
        except ValueError:
            raise Exception("その曲は登録されてないよ！")

        # プレイリストを更新する
        playlistApplicationService.save(playlist)

    # ---------------------
