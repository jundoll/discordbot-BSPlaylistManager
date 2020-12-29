
# load modules
import uuid
import inject
from Domain.Playlist import Playlist, PlaylistAuthor, PlaylistDescription, PlaylistFileName, PlaylistId, PlaylistInfo, PlaylistTitle
from DomainService.PlaylistService import PlaylistService
from Repository.PlaylistRepository import IPlaylistRepository
from Temp.PlaylistUpdateCommand import PlaylistUpdateCommand


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

    # タイトルに一致するプレイリストを検索する
    def find(self, title: str) -> Playlist:
        playlistTitle = PlaylistTitle(title)
        foundPlaylist = self.playlistRepository.findPlaylistByTitle(
            playlistTitle)
        return foundPlaylist

    # 指定のプレイリストを保存する
    def save(self, playlist: Playlist):
        self.playlistRepository.save(playlist)

    # ---------------------

    # 空のプレイリストを新規作成する
    def create(self, title: str):

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
            playlistAuthor=PlaylistAuthor(""),
            playlistDescription=PlaylistDescription(
                "This is generated by discordbot-BSPlaylistManager."),
            image=playlistService.encodeImage(),
            songs=list()
        )

        # create new playlist
        playlistService.create(playlist)

    # ---------------------

    # 既存のプレイリストを削除する
    def delete(self, title: str):

        # create new playlist
        playlistTitle = PlaylistTitle(title)
        self.playlistRepository.delete(playlistTitle)

    # ---------------------

    def getDownloadUrl(self, title: str) -> str:
        playlistTitle = PlaylistTitle(title)
        self.playlistRepository.getDownloadUrl(playlistTitle)

    # ---------------------

    # プレイリスト情報を更新する（今後実装）
    def update(self, command: PlaylistUpdateCommand):
        pass


class PlaylistUpdateCommand:
    def playlistUpdateCommand(self, id: str):
        pass