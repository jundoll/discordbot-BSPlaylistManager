
# load modules
import uuid
import inject
from Domain.Playlist import Playlist, PlaylistAuthor, PlaylistDescription, PlaylistFileName, PlaylistId, PlaylistInfo, PlaylistTitle
from DomainService.PlaylistService import PlaylistService
from Repository.PlaylistRepository import IPlaylistRepository


# definition
class PlaylistApplicationService:
    # 凝集度などの問題で分割が必要になったら分ける

    # instance fields
    playlistRepository: IPlaylistRepository = inject.attr(IPlaylistRepository)

    # post init
    def __post__init__(self):

        # type check
        if not isinstance(self.playlistRepository, IPlaylistRepository):
            raise Exception

    # ---------------------

    # タイトルからプレイリストを取得する
    def find(self, title: str) -> Playlist:

        # type check
        if not isinstance(title, str):
            raise Exception

        # タイトルからプレイリストを取得する
        playlistService = PlaylistService()
        playlistTitle = PlaylistTitle(title)
        playlist = playlistService.findPlaylist(playlistTitle)
        return playlist

    # プレイリストを更新する
    def save(self, playlist: Playlist):

        # プレイリストを更新する
        self.playlistRepository.savePlaylist(playlist)

    # ---------------------

    # 空のプレイリストを新規作成する
    def create(self, title: str):

        # type check
        if not isinstance(title, str):
            raise Exception

        # set paramter
        playlistInfo = PlaylistInfo(
            playlistId=PlaylistId(str(uuid.uuid4())),
            playlistFileName=PlaylistFileName(title),
            playlistTitle=PlaylistTitle(title)
        )

        # define new playlist
        # authorはサーバ名で標準設定したい（今後実装検討）
        playlistService = PlaylistService()
        playlist = Playlist(
            playlistInfo=playlistInfo,
            playlistTitle=playlistInfo.playlistTitle,
            playlistAuthor=PlaylistAuthor("discordbot-BSPlaylistManager"),
            playlistDescription=PlaylistDescription(
                "This is generated by discordbot-BSPlaylistManager."),
            image=playlistService.encodeImage(),
            songs=[]
        )

        # 空のプレイリストを新規作成する
        playlistService.create(playlist)

    # ---------------------

    # 既存のプレイリストを削除する
    def delete(self, title: str):

        # type check
        if not isinstance(title, str):
            raise Exception

        # 既存のプレイリストを削除する
        playlistTitle = PlaylistTitle(title)
        self.playlistRepository.deletePlaylist(playlistTitle)

    # ---------------------

    # タイトルからプレイリストのダウンロードURLを取得する
    def getDownloadUrl(self, title: str) -> str:

        # タイトルからプレイリストのダウンロードURLを取得する
        playlistTitle = PlaylistTitle(title)
        url = self.playlistRepository.getDownloadUrl(playlistTitle)
        return url

    # ---------------------
