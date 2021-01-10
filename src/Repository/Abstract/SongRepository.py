
# load modules
from abc import ABCMeta, abstractmethod
from typing import Union
from src.Domain.Song import Song, SongHash, SongID


# definition
class ISongRepository(metaclass=ABCMeta):

    # 曲IDに対応する曲情報を新規登録または更新する
    @abstractmethod
    def upsert(self, song: Song):
        pass

    # 曲IDに対応する曲情報を削除する
    @abstractmethod
    def delete(self, songID: SongID):
        pass

    # 曲IDからhash値を読み込む
    @abstractmethod
    def findHashByID(self, songID: SongID) -> Union[Song, None]:
        pass

    # hash値から曲情報を読み込む
    @abstractmethod
    def findByHash(self, songHash: SongHash) -> Union[Song, None]:
        pass
