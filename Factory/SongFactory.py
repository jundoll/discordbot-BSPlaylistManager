
# load modules
from lxml import html
from abc import ABCMeta, abstractmethod
from Domain.Song import Song
from urllib import request


# definition
class ISongFactory(metaclass=ABCMeta):

    # URLからSongインスタンスを生成する
    @abstractmethod
    def create(self, url: str) -> Song:
        pass


class SongFactory(ISongFactory):

    # URLからSongインスタンスを生成する
    def create(self, url: str) -> Song:

        # URLからhash値を取得する
        if "/bsaber.com/" in url:
            try:
                hash = self._scrapeHashFromBsaber(url)
            except Exception:
                raise Exception("bsaber.com との通信に失敗したよ！")
        else:
            raise Exception("bsaber.com から曲を検索してね！")

        # hash値からSongインスタンスを生成する
        song = Song(hash)
        return song

    def _scrapeHashFromBsaber(self, url: str) -> str:

        # URLのページをスクレイピングする
        data = request.urlopen(url)
        raw_html = data.read()
        format_html = html.fromstring(str(raw_html))

        # hash値を取得する
        dl_url = format_html.xpath(
            '//*[@id="infinite-article"]/div[1]/div[1]/div[2]/div/div/header/div[4]/a[3]/@href')[0]
        hash = dl_url.split('/')[-1].split('.')[0]
        return hash
