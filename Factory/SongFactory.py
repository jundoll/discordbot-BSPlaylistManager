
# load modules
from DomainService.SongService import SongService
from Domain.Song import Song
from abc import ABCMeta, abstractmethod


# definition
class ISongFactory(ABCMeta):

    # URLからSongインスタンスを生成する
    @abstractmethod
    def create(self, url: str) -> Song:
        pass


class SongFactory(ISongFactory):

    # URLからSongインスタンスを生成する
    def create(self, url: str) -> Song:
        self.songService = SongService()
        song = self.songService.getFromURL(url)
        return song
