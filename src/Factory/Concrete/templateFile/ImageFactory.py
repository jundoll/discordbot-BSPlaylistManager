
# load modules
import base64
from src.Domain.Playlist import ImageBase64, PlaylistKeyword
from src.Factory.Abstract.ImageFactory import IImageFactory
from urllib import request


# definition
class ImageFactory(IImageFactory):

    # キーワードに基づき画像を生成する
    def generateByKeyword(self, keyword: PlaylistKeyword) -> ImageBase64:

        with open("Image/template.png", "rb") as f:
            encodedImage = base64.b64encode(f.read()).decode("utf-8")
            image = ImageBase64(
                "data:image/png;base64," + encodedImage)
            return image

    # 指定ファイルから画像を生成する
    def convertByImageFile(self, imageUrl: str) -> ImageBase64:

        # encode base64
        encodedImage = base64.b64encode(
            request.urlopen(imageUrl).read()).decode("utf-8")
        if imageUrl.endswith("png"):
            image = ImageBase64("data:image/png;base64," + encodedImage)
        elif imageUrl.endswith(("jpg", "jpeg")):
            image = ImageBase64("data:image/jpeg;base64," + encodedImage)
        else:
            raise Exception("png または jpg(jpeg) ファイルを指定してね！")
        return image
