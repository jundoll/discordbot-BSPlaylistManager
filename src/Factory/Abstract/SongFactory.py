
# load modules
from abc import ABCMeta, abstractmethod
from typing import List
from src.Domain.Song import Song, SongHash, Url


# definition
class ISongFactory(metaclass=ABCMeta):

    # URLからSongインスタンスのリストを生成する
    @abstractmethod
    def generateByUrl(self, url: Url) -> List[Song]:
        pass

    # hash値からSongインスタンスを生成する
    @abstractmethod
    def generateByHash(self, hash: SongHash) -> Song:
        pass
