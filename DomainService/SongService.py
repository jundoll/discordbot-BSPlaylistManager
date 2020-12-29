
# load modules
from urllib import request
from Domain.Song import Song
from lxml import html


# definition
class SongService:

    def getFromURL(self, url: str) -> Song:

        # scrape hash string
        if "//bsaber.com" in url:
            try:
                hash = self._scrapeHashFromBsaber(url)
            except Exception:
                raise Exception("bsaber.com との通信に失敗したよ！")
        else:
            raise Exception("bsaber.com から曲を検索してね！")

        # return
        song = Song(hash)
        return song

    def _scrapeHashFromBsaber(self, url: str) -> str:

        data = request.urlopen(url)
        raw_html = data.read()
        format_html = html.fromstring(str(raw_html))

        # hash値
        dl_url = format_html.xpath(
            '//*[@id="infinite-article"]/div[1]/div[1]/div[2]/div/div/header/div[4]/a[3]/@href')[0]
        hash = dl_url.split('/')[-1].split('.')[0]
        return hash
