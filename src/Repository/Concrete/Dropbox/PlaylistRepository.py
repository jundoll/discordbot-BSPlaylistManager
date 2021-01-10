
# load modules
import re
from typing import List, Union
from Message.Error import OriginalException
from Message.Message import ErrorMessages
from src.Domain.Playlist import (ImageBase64, Playlist, PlaylistAuthor, PlaylistDescription,
                                 PlaylistFileName, PlaylistID, PlaylistKeyword, PlaylistTitle, SearchKeyword)
from src.Domain.Song import SongID
from src.Repository.Abstract.PlaylistRepository import IPlaylistRepository
from src.Repository.Concrete.Dropbox.DropboxHandler import DropboxHandler


# definition
class PlaylistRepository(IPlaylistRepository):

    def __init__(self):
        self.handler = DropboxHandler()

    # ---------------------

    # プレイリストを新規登録する
    def insertPlaylist(self, playlist: Playlist):

        # read DB
        playlistDB = self.handler.readJsonFile(self.handler.PLAYLIST_DB_PATH)
        if playlistDB is None:
            playlistDB = {
                "playlistID": [],
                "fileName": [],
                "keyword": [],
                "playlistTitle": [],
                "playlistAuthor": [],
                "playlistDescription": [],
                "image": [],
                "isDeleted": []
            }

        # insert
        if playlist.playlistID.ID in playlistDB["playlistID"]:
            # プレイリストID UNIQUE制約エラー
            raise OriginalException(
                ErrorMessages.uniquePlaylistPlaylistIDErrorMessage())
        else:
            playlistDB["playlistID"].append(playlist.playlistID.ID)
            playlistDB["fileName"].append(playlist.fileName.filename)
            playlistDB["keyword"].append(playlist.keyword.keyword)
            playlistDB["playlistTitle"].append(playlist.title.title)
            playlistDB["playlistAuthor"].append(playlist.author.author)
            playlistDB["playlistDescription"].append(
                playlist.description.description)
            playlistDB["image"].append(playlist.image.image)
            playlistDB["isDeleted"].append(False)

        # delete deleted Playlist
        if playlist.keyword.keyword in playlistDB["keyword"]:

            # delete the playlist
            deletePlaylistID = ""
            for i, keyword in enumerate(playlistDB["keyword"]):
                if (playlist.keyword.keyword == keyword) & (playlistDB["isDeleted"][i]):
                    deletePlaylistID = playlistDB["playlistID"][i]
                    del playlistDB["playlistID"][i]
                    del playlistDB["fileName"][i]
                    del playlistDB["keyword"][i]
                    del playlistDB["playlistTitle"][i]
                    del playlistDB["playlistAuthor"][i]
                    del playlistDB["playlistDescription"][i]
                    del playlistDB["image"][i]
                    del playlistDB["isDeleted"][i]
                    break

            # delete the playlistDetail
            if len(deletePlaylistID) > 0:
                # read
                playlistDetailDB = self.handler.readJsonFile(
                    self.handler.PLAYLIST_DETAIL_DB_PATH)
                if playlistDetailDB is not None:
                    # delete
                    for i, playlistID in enumerate(playlistDetailDB["playlistID"]):
                        if deletePlaylistID == playlistID:
                            del playlistDetailDB["detailID"][i]
                            del playlistDetailDB["playlistID"][i]
                            del playlistDetailDB["songID"][i]
                    # save
                    self.handler.saveJsonFile(
                        playlistDetailDB, self.handler.PLAYLIST_DETAIL_DB_PATH)

        # save DB
        self.handler.saveJsonFile(playlistDB, self.handler.PLAYLIST_DB_PATH)

    # プレイリストIDに対応するプレイリストの削除フラグをオンにする
    def deletePlaylist(self, playlistID: PlaylistID):

        # read DB
        playlistDB = self.handler.readJsonFile(self.handler.PLAYLIST_DB_PATH)
        if playlistDB is None:
            return

        # update
        if playlistID.ID not in playlistDB["playlistID"]:
            for i, ID in enumerate(playlistDB["playlistID"]):
                if playlistID.ID == ID:
                    playlistDB["isDeleted"][i] = True
                    break

        # save DB
        self.handler.saveJsonFile(playlistDB, self.handler.PLAYLIST_DB_PATH)

    # プレイリストIDに対応するプレイリストの削除フラグをオフにする
    def restorePlaylist(self, playlistID: PlaylistID):

        # read DB
        playlistDB = self.handler.readJsonFile(self.handler.PLAYLIST_DB_PATH)
        if playlistDB is None:
            return

        # update
        if playlistID.ID not in playlistDB["playlistID"]:
            for i, ID in enumerate(playlistDB["playlistID"]):
                if playlistID.ID == ID:
                    playlistDB["isDeleted"][i] = False
                    break

        # save DB
        self.handler.saveJsonFile(playlistDB, self.handler.PLAYLIST_DB_PATH)

    # プレイリストIDからプレイリストを読み込む
    def findByID(self, playlistID: PlaylistID) -> Union[Playlist, None]:

        # read DB
        playlistDB = self.handler.readJsonFile(self.handler.PLAYLIST_DB_PATH)
        if playlistDB is None:
            return
        playlistDetailDB = self.handler.readJsonFile(
            self.handler.PLAYLIST_DETAIL_DB_PATH)
        if playlistDetailDB is None:
            return

        # get song
        songIDs = []
        for i, ID in enumerate(playlistDetailDB["playlistID"]):
            if playlistID.ID == ID:
                songIDs.append(playlistDetailDB["songID"][i])

        # set playlist
        for i, ID in enumerate(playlistDB["playlistID"]):
            if playlistID.ID == ID:
                playlist = Playlist(
                    playlistID=playlistID,
                    fileName=PlaylistFileName(playlistDB["fileName"][i]),
                    keyword=PlaylistKeyword(playlistDB["keyword"][i]),
                    title=PlaylistTitle(playlistDB["playlistTitle"][i]),
                    author=PlaylistAuthor(playlistDB["playlistAuthor"][i]),
                    description=PlaylistDescription(
                        playlistDB["playlistDescription"][i]),
                    image=ImageBase64(playlistDB["image"][i]),
                    songIDs=songIDs
                )
                # return
                return playlist

    # キーワードからプレイリストを読み込む
    def findByKeyword(self, playlistKeyword: PlaylistKeyword) -> Union[Playlist, None]:

        # read DB
        playlistDB = self.handler.readJsonFile(self.handler.PLAYLIST_DB_PATH)
        if playlistDB is None:
            return
        playlistDetailDB = self.handler.readJsonFile(
            self.handler.PLAYLIST_DETAIL_DB_PATH)
        if playlistDetailDB is None:
            return

        # get playlistID
        playlistID = ""
        if playlistKeyword.keyword in playlistDB["keyword"]:
            for i, keyword in enumerate(playlistDB["keyword"]):
                if playlistKeyword.keyword == keyword:
                    playlistID = playlistDB["playlistID"][i]
                    break
        if len(playlistID) == 0:
            return

        # get song
        songIDs = []
        for i, ID in enumerate(playlistDetailDB["playlistID"]):
            if playlistID == ID:
                songIDs.append(playlistDetailDB["songID"][i])

        # set playlist
        for i, ID in enumerate(playlistDB["playlistID"]):
            if playlistID == ID:
                playlist = Playlist(
                    playlistID=PlaylistID(playlistID),
                    fileName=PlaylistFileName(playlistDB["fileName"][i]),
                    keyword=playlistKeyword,
                    title=PlaylistTitle(playlistDB["playlistTitle"][i]),
                    author=PlaylistAuthor(playlistDB["playlistAuthor"][i]),
                    description=PlaylistDescription(
                        playlistDB["playlistDescription"][i]),
                    image=ImageBase64(playlistDB["image"][i]),
                    songIDs=songIDs
                )
                # return
                return playlist

    # キーワードからプレイリストIDを読み込む
    def findIDByKeyword(self, playlistKeyword: PlaylistKeyword, isDeleted: bool = False) -> Union[PlaylistID, None]:

        # read DB
        playlistDB = self.handler.readJsonFile(self.handler.PLAYLIST_DB_PATH)
        if playlistDB is None:
            return
        playlistDetailDB = self.handler.readJsonFile(
            self.handler.PLAYLIST_DETAIL_DB_PATH)
        if playlistDetailDB is None:
            return

        # get playlistID
        playlistID = ""
        if playlistKeyword.keyword in playlistDB["keyword"]:
            for i, keyword in enumerate(playlistDB["keyword"]):
                if (playlistKeyword.keyword == keyword) & (playlistDB["isDeleted"] == isDeleted):
                    playlistID = playlistDB["playlistID"][i]
                    return playlistID
        if len(playlistID) == 0:
            return

    # プレイリスト情報を更新する
    def update(self, playlist: Playlist):

        # read DB
        playlistDB = self.handler.readJsonFile(self.handler.PLAYLIST_DB_PATH)
        if playlistDB is None:
            return

        # update
        if playlist.playlistID.ID not in playlistDB["playlistID"]:
            for i, ID in enumerate(playlistDB["playlistID"]):
                if playlist.playlistID.ID == ID:
                    playlistDB["fileName"][i] = playlist.fileName.filename
                    if playlist.keyword.keyword != playlistDB["keyword"][i]:
                        if playlist.keyword.keyword in playlistDB["keyword"]:
                            # キーワード UNIQUE制約エラー
                            raise OriginalException(
                                ErrorMessages.uniquePlaylistKeywordErrorMessage())
                        else:
                            playlistDB["keyword"][i] = playlist.keyword.keyword
                    playlistDB["playlistTitle"][i] = playlist.title.title
                    playlistDB["playlistAuthor"][i] = playlist.author.author
                    playlistDB["playlistDescription"][i] = playlist.description.description
                    playlistDB["image"][i] = playlist.image.image
                    break

        # save DB
        self.handler.saveJsonFile(playlistDB, self.handler.PLAYLIST_DB_PATH)

    # プレイリストへ曲を新規登録する
    def insertSong(self, playlistID: PlaylistID, songID: SongID):

        # read DB
        playlistDetailDB = self.handler.readJsonFile(
            self.handler.PLAYLIST_DETAIL_DB_PATH)
        if playlistDetailDB is None:
            playlistDetailDB = {
                "detailID": [],
                "playlistID": [],
                "songID": []
            }

        # exists check
        existsFlag = False
        for i in range(len(playlistDetailDB["detailID"])):
            if (playlistID.ID == playlistDetailDB["playlistID"][i]) & (songID.ID == playlistDetailDB["songID"][i]):
                existsFlag = True
                break

        # insert
        if not existsFlag:
            # insert
            detailIDs = [int(ID)for ID in playlistDetailDB["detailID"]]
            playlistDetailDB["detailID"].append(str(1+max(detailIDs)))
            playlistDetailDB["playlistID"].append(playlistID.ID)
            playlistDetailDB["songID"].append(songID.ID)

        # save DB
        self.handler.saveJsonFile(
            playlistDetailDB, self.handler.PLAYLIST_DETAIL_DB_PATH)

    # プレイリストから曲を削除する
    def deleteSong(self, playlistID: PlaylistID, songID: SongID):

        # read DB
        playlistDetailDB = self.handler.readJsonFile(
            self.handler.PLAYLIST_DETAIL_DB_PATH)
        if playlistDetailDB is None:
            return

        # delete song
        for i in range(len(playlistDetailDB["detailID"])):
            if (playlistID.ID == playlistDetailDB["playlistID"][i]) & (songID.ID == playlistDetailDB["songID"][i]):
                del playlistDetailDB["detailID"][i]
                del playlistDetailDB["playlistID"][i]
                del playlistDetailDB["songID"][i]

        # save DB
        self.handler.saveJsonFile(
            playlistDetailDB, self.handler.PLAYLIST_DETAIL_DB_PATH)

    # 検索キーワードに対応する全てのプレイリストを読み込む
    def fuzzyFindByKeyword(self, searchKeyword: SearchKeyword) -> Union[List[Playlist], None]:

        # read DB
        playlistDB = self.handler.readJsonFile(self.handler.PLAYLIST_DB_PATH)
        if playlistDB is None:
            return
        playlistDetailDB = self.handler.readJsonFile(
            self.handler.PLAYLIST_DETAIL_DB_PATH)
        if playlistDetailDB is None:
            return

        # get playlists
        playlists = []
        for keyword in playlistDB["keyword"]:
            if re.search(searchKeyword.searchKeyword, keyword) is not None:
                playlist = self.findByKeyword(PlaylistKeyword(keyword))
                playlists.append(playlist)

        # return
        return playlists

    # ---------------------
