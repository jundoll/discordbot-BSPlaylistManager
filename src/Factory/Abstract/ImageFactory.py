
# load modules
from abc import ABCMeta, abstractmethod
from src.Domain.Playlist import ImageBase64, PlaylistKeyword


# definition
class IImageFactory(metaclass=ABCMeta):

    # キーワードに基づき画像を生成する
    @abstractmethod
    def generateByKeyword(self, keyword: PlaylistKeyword) -> ImageBase64:
        pass

    # 指定ファイルから画像を生成する
    @abstractmethod
    def convertByImageFile(self, imageUrl: str) -> ImageBase64:
        pass
