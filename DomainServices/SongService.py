
# load modules
from typing import Dict, List
from Domains.Song import Song, SongList
from urllib import request
from lxml import html


# definition
class SongService:

    def scrapeHashFromBsaber(self, url: str) -> str:

        data = request.urlopen(url)
        raw_html = data.read()
        format_html = html.fromstring(str(raw_html))

        # hash値
        dl_url = format_html.xpath(
            '//*[@id="infinite-article"]/div[1]/div[1]/div[2]/div/div/header/div[4]/a[3]/@href')[0]
        hash = dl_url.split('/')[-1].split('.')[0]
        return hash

    def getFromURL(self, url: str) -> Song:

        hash = None
        for url_split in url.split('/'):
            if url_split == 'bsaber.com':
                hash = self.scrapeHashFromBsaber(url)
                break

        if hash is None:
            raise Exception

        # return
        song = Song(hash)
        return song


class SongListService:

    def load(self, songList: SongList):
        self.songList = songList

    def add(self, url: str):
        pass

    def delete(self):
        pass
