
# load modules
from urllib.request import urlopen
import datetime
from urllib.request import Request
import uuid
import inject
from Domain.Playlist import ImageBase64, Playlist, PlaylistInfo, PlaylistTitle
from Repository.PlaylistRepository import IPlaylistRepository
from DomainService.SongService import SongService
import base64


# definition
class PlaylistService:

    # instance fields
    playlistRepository: IPlaylistRepository = inject.attr(IPlaylistRepository)

    # post init
    def __post_init__(self):

        # type check
        if not isinstance(self.playlistRepository, IPlaylistRepository):
            raise Exception

    # 画像をbase64変換する
    def encodeImage(self, imageUrl: str = "") -> ImageBase64:

        # if empty
        if len(imageUrl) == 0:
            with open("Image/template.png", "rb") as f:
                encodedImage = base64.b64encode(f.read()).decode("utf-8")
                image = ImageBase64("data:image/png;base64," + encodedImage)
                return image

        # encode base64
        encodedImage = base64.b64encode(
            urlopen(imageUrl).read()).decode("utf-8")
        if imageUrl.endswith("png"):
            image = ImageBase64("data:image/png;base64," + encodedImage)
        elif imageUrl.endswith(("jpg", "jpeg")):
            image = ImageBase64("data:image/jpeg;base64," + encodedImage)
        else:
            raise Exception("png または jpg(jpeg) ファイルを指定してね！")
        return image

    # 空のプレイリストを新規作成する
    def create(self, playlist: Playlist):

        # depulicated check
        if self._exists(playlist.playlistInfo):
            raise Exception("既に存在するタイトルだよ！違う名前に変えてね！")

        # save
        self.playlistRepository.create(playlist)

    # 指定タイトルのプレイリストが存在するかどうか
    def _exists(self, playlistInfo: PlaylistInfo) -> bool:
        foundPlaylist = self.playlistRepository.findPlaylistByTitle(
            playlistInfo.playlistTitle)
        return foundPlaylist is not None

    # ------------------------

    # register info list
    # ここに定義すべき？微妙。
    def registerInfoList(self, ):
        pass

    # change info
    def changeInfo(self, keyword: str, info: str):
        playlist = self.search(keyword)

    # get playlist
    def show(self) -> Playlist:
        pass

    # parse to json
    def parse2json(self, playlist: Playlist):
        pass
