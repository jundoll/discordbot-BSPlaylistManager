
# load modules
from Domain.Song import Song
from typing import Dict, List, Union
from Domain.Playlist import ImageBase64, Playlist, PlaylistAuthor, PlaylistDescription, PlaylistFileName, PlaylistId, PlaylistInfo, PlaylistTitle
import csv
import json
import os
from urllib import request

import dropbox

# init settings
is_dev = os.environ['IS_DEV_BINARY'] == str(1)
dropbox_token = os.environ['DROPBOX_ACCESS_TOKEN']
dropbox_path = 'BSPlaylistManager-dev' if is_dev else 'BSPlaylistManager'


# definition
class Dropbox:
    # dropboxもapplicationserviceを作ってもいいかもしれない

    def __init__(self):
        self.dbx = dropbox.Dropbox(dropbox_token)
        self.dpathInfoList = "/{}/PlaylistInfoList".format(dropbox_path)
        self.fpathInfoList = "{}/infoList.csv".format(self.dpathInfoList)
        self.dpathPlaylist = "/{}/Playlists".format(dropbox_path)

    # タイトルからプレイリスト情報を取得する
    def findInfoByTitle(self, playlistTitle: PlaylistTitle) -> Union[PlaylistInfo, None]:

        # read info list
        infoList = self._readInfoList()

        # find info by title
        if infoList is not None:
            for info in infoList:
                if info.playlistTitle == playlistTitle:
                    return info

    # プレイリスト情報一覧を読み込む
    def _readInfoList(self) -> Union[List[PlaylistInfo], None]:

        # get file and folder list
        entryList = self._findPathList(self.dpathPlaylist)
        # if the folder does not exists
        if len(entryList) == 0:
            self.dbx.files_create_folder_v2(self.dpathPlaylist)
            self._createInfoList()
            return

        # get file list
        fileEntryList = self._findPathList(self.dpathPlaylist+"/", entryList)
        fileList = [entry.path_lower for entry in fileEntryList]

        # read info list
        infoList = []
        for file in fileList:
            with open(file) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    info = PlaylistInfo(
                        PlaylistId(row["ID"]),
                        PlaylistFileName(row["FileName"]),
                        PlaylistTitle(row["Title"]))
                    infoList += [info]
                return infoList
        # if the file does not exists
        if len(infoList) == 0:
            self._createInfoList()
            return

    # 指定の文字列を含むフォルダ・ファイルパスの一覧を返す
    def _findPathList(self, keyword: str, entryList: list = list()) -> List[str]:
        res = self.dbx.files_list_folder("", recursive=True)
        entryList += [
            entry for entry in res.entries if (keyword in entry.path_display)]
        return entryList

    # プレイリスト情報一覧を新規作成する
    def _createInfoList(self):

        # create info list file
        fileList = self._findPathList(self.fpathInfoList)
        if len(fileList) == 0:
            with open(self.fpathInfoList, "w") as f:
                writer = csv.DictWriter(f, list(["ID", "FileName", "Title"]))
                writer.writeheader()

    # ----------------------------------

    # プレイリストを読み込む
    def readPlaylistJsonByFileName(self, playlistFileName: PlaylistFileName) -> Playlist:

        # set file path
        filePath = "{}/{}.json".format(self.dpathPlaylist,
                                       playlistFileName.playlistFileName)

        # load playlist
        playlistJson = request.urlopen(filePath).read()
        playlistJson = json.loads(playlistJson)

        # convert playlist from dict(json)
        playlist = self._convertPlaylistFromJson(playlistJson)
        return playlist

    # プレイリストを json 形式から変換する
    def _convertPlaylistFromJson(self, playlistJson: dict) -> Playlist:

        # key exists check
        playlistKeys = ["playlistTitle", "playlistAuthor",
                        "playlistDescription", "image", "songs"]
        if set(playlistJson.keys()) != playlistKeys:
            raise Exception("プレイリストの読み込み中にエラーが発生したよ！")

        # get info
        playlistInfo = self.findInfoByTitle(playlistJson["playlistTitle"])
        if playlistInfo is None:
            raise Exception("指定のプレイリストが見つからないよ！")

        # convert
        playlist = Playlist(
            playlistInfo=playlistInfo,
            playlistTitle=playlistJson["playlistTitle"],
            playlistAuthor=PlaylistAuthor(playlistJson["playlistAuthor"]),
            playlistDescription=PlaylistDescription(
                playlistJson["playlistDescription"]),
            image=ImageBase64(playlistJson["image"]),
            songs=[Song(songDict.hash) for songDict in playlistJson["songs"]]
        )

        # return
        return playlist

    # ----------------------------------

    # プレイリストを保存する
    def savePlaylistJson(self, playlist: Playlist):

        # set file path
        filePath = "{}/{}.json".format(self.dpathPlaylist,
                                       playlist.playlistInfo.playlistFileName.playlistFileName)

        # convert playlist into dict(json)
        playlistJson = {
            "playlistTitle": playlist.playlistTitle.playlistTitle,
            "playlistAuthor": playlist.playlistAuthor.playlistAuthor,
            "playlistDescription": playlist.playlistDescription.playlistDescription,
            "image": playlist.image.image,
            "songs": [song.convertJson() for song in playlist.songs]
        }

        # update playlist
        playlistBytes = bytes(json.dumps(playlistJson, separators=(
            ',', ':'), ensure_ascii=False), encoding="utf-8")
        self.dbx.files_upload(playlistBytes, filePath,
                              mode=dropbox.files.WriteMode.overwrite)

    # ----------------------------------

    # 指定のプレイリスト情報を情報一覧に追加する
    # playlistのように一度読み込んで書き込む方がスマートかも？
    def registerInfo(self, info: PlaylistInfo):

        # convert info into dict
        infoDict = {
            "ID": info.playlistId,
            "FileName": info.playlistFileName,
            "Title": info.playlistTitle
        }

        # register info
        fileList = self._findPathList(self.fpathInfoList)
        if len(fileList) == 0:
            # 新規作成
            self._createInfoList()

        with open(self.fpathInfoList, "a") as f:
            writer = csv.DictWriter(f, list(infoDict.keys()))
            writer.writerow(infoDict)

    # ----------------------------------

    # 指定のパスが存在するかどうかを返す
    def _fileExistsInfoList(self, filePath: str) -> bool:
        fileList = self._findPathList(filePath)
        return len(fileList) == 0

    def unregisterInfo(self, info: PlaylistInfo, playlistFileName: PlaylistFileName = PlaylistFileName("infoList")):
        # set file path
        filePath = "{}/{}.csv".format(
            self.dpathInfoList, playlistFileName.playlistFileName)
        # unregister info
        with open(filePath, "a") as f:
            writer = csv.DictWriter(f, ["ID", "FileName", "Title"])
            writer.writerow(info)

    def makePlaylistPath(self):
        pass

    def saveInfoList(self, filePath: str, info: dict, isNew: bool = False):
        if isNew:
            # 新規作成
            with open(filePath, "w") as f:
                writer = csv.DictWriter(f, ["ID", "FileName", "Title"])
                writer.writeheader()
        else:
            # 既存追加
            with open(filePath, "a") as f:
                writer = csv.DictWriter(f, ["ID", "FileName", "Title"])
                writer.writerow(info)

    def getFileNameById(self, id: PlaylistId) -> Union[PlaylistFileName, None]:
        infoList = self.readInfoList()
        if len(infoList) == 0:
            pass
        else:
            for info in infoList:
                if info.playlistId == id:
                    return info.playlistFileName

    def getFilePathList(self) -> List:
        res = self.dbx.files_list_folder("", recursive=True)
        for entry in res.entries:
            if entry.path_display.startswith("/"+dropbox_path+"/"):
                self.fpath = entry.path_lower

    def getSharedLink(self):
        links = self.dbx.sharing_list_shared_links(
            path=self.fpath, direct_only=True).links

        if links is not None:
            for link in links:
                return link.url.replace("dl=0", "dl=1")

        return self.createSharedLink()

    def createSharedLink(self):
        setting = dropbox.sharing.SharedLinkSettings(
            requested_visibility=dropbox.sharing.RequestedVisibility.public)
        link = self.dbx.sharing_create_shared_link_with_settings(
            path=self.fpath, settings=setting)

        return link.url.replace("dl=0", "dl=1")
