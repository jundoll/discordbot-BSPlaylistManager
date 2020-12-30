
# load modules
import base64
from urllib.request import urlopen
import inject
from Domain.Playlist import ImageBase64, Playlist, PlaylistTitle
from Repository.PlaylistRepository import IPlaylistRepository


# definition
class PlaylistService:

    # instance fields
    playlistRepository: IPlaylistRepository = inject.attr(IPlaylistRepository)

    # post init
    def __post_init__(self):

        # type check
        if not isinstance(self.playlistRepository, IPlaylistRepository):
            raise Exception

    # ---------------------

    # タイトルからプレイリストを取得する
    def findPlaylist(self, playlistTitle: PlaylistTitle) -> Playlist:

        # type check
        if not isinstance(playlistTitle, PlaylistTitle):
            raise Exception

        # タイトルからプレイリストを取得する
        playlist = self.playlistRepository.readPlaylist(playlistTitle)
        if playlist is None:
            raise Exception("指定のプレイリストが見つからないよ！")
            # エラーケース
            # ・プレイリスト情報一覧が見つからない
            # ・プレイリスト情報一覧に一致するタイトルが見つからない
            # ・タイトルに一致するプレイリストが見つからない
        else:
            return playlist

    # ------------------------

    # 空のプレイリストを新規作成する
    def create(self, playlist: Playlist):

        # type check
        if not isinstance(playlist, Playlist):
            raise Exception

        # save info
        self.playlistRepository.registerInfo(playlist.playlistInfo)

        # save playlist
        self.playlistRepository.savePlaylist(playlist)

    # ------------------------

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

    # ------------------------

    # change info
    def changeInfo(self, keyword: str, info: str):
        pass

    # get playlist
    def show(self) -> Playlist:
        pass

    # parse to json
    def parse2json(self, playlist: Playlist):
        pass
