
# load modules
import base64
import aiohttp
from src.Message.Error import OriginalException
from src.Message.Message import ErrorMessages
from src.Domain.Playlist import ImageBase64, PlaylistKeyword
from src.Factory.Abstract.ImageFactory import IImageFactory


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
    async def convertByImageFile(self, imageUrl: str) -> ImageBase64:

        # encode base64
        async with aiohttp.ClientSession() as session:
            async with session.get(imageUrl) as r:
                if r.status == 200:
                    readImage = await r.read()
                    encodedImage = base64.b64encode(readImage).decode()
                else:
                    raise OriginalException(
                        ErrorMessages.DownloadImageFileErrorMessage)

        if imageUrl.endswith("png"):
            image = ImageBase64("data:image/png;base64," + encodedImage)
        elif imageUrl.endswith(("jpg", "jpeg")):
            image = ImageBase64("data:image/jpeg;base64," + encodedImage)
        else:
            raise Exception("png または jpg(jpeg) ファイルを指定してね！")
        return image
