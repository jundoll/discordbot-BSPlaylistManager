
# load modules
from abc import ABCMeta, abstractmethod
from Domain.Song import Song
from DomainService.SongService import SongService


# definition
class ISongFactory(metaclass=ABCMeta):

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
