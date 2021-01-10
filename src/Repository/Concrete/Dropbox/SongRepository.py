
# load modules
from typing import Union
from src.Domain.Song import Song, SongHash, SongID
from src.Repository.Abstract.SongRepository import ISongRepository
from src.Repository.Concrete.Dropbox.DropboxHandler import DropboxHandler


# definition
class SongRepository(ISongRepository):

    def __init__(self):
        self.handler = DropboxHandler()

    # ---------------------

    # 曲IDに対応する曲情報を新規登録または更新する
    def upsert(self, song: Song):

        # read song DB
        songDB = self.handler.readJsonFile(self.handler.SONG_DB_PATH)
        if songDB is None:
            songDB = {
                "songID": [],
                "hash": []
            }

        # upsert
        if song.songID.ID in songDB["songID"]:
            # update
            for i, songID in enumerate(songDB["songID"]):
                if song.songID.ID == songID:
                    songDB["hash"][i] = song.hash.hash
                    break
        else:
            # insert
            songDB["songID"].append(song.songID.ID)
            songDB["hash"].append(song.hash.hash)

        # save song DB
        self.handler.saveJsonFile(songDB, self.handler.SONG_DB_PATH)

    # 曲IDに対応する曲情報を削除する
    def delete(self, songID: SongID):

        # read song DB
        songDB = self.handler.readJsonFile(self.handler.SONG_DB_PATH)
        if songDB is None:
            return

        # delete
        for i, ID in enumerate(songDB["songID"]):
            if songID.ID == ID:
                del songDB["songID"][i]
                del songDB["hash"][i]
                break

        # save song DB
        self.handler.saveJsonFile(songDB, self.handler.SONG_DB_PATH)

    # 曲IDからhash値を読み込む
    def findHashByID(self, songID: SongID) -> Union[Song, None]:

        # read song DB
        songDB = self.handler.readJsonFile(self.handler.SONG_DB_PATH)
        if songDB is None:
            return

        # set Song instance
        for i, ID in enumerate(songDB["songID"]):
            if songID.ID == ID:
                song = Song(
                    songID=songID,
                    hash=SongHash(songDB["hash"][i])
                )
                # return
                return song

    # hash値から曲情報を読み込む
    def findByHash(self, songHash: SongHash) -> Union[Song, None]:

        # read song DB
        songDB = self.handler.readJsonFile(self.handler.SONG_DB_PATH)
        if songDB is None:
            return

        # set Song instance
        for i, hash in enumerate(songDB["hash"]):
            if songHash.hash == hash:
                song = Song(
                    songID=SongID(songDB["songID"][i]),
                    hash=songHash
                )
                # return
                return song
