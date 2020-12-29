
# load modules
import csv
import json
import os
from typing import List, Union
from urllib import request
import dropbox
from Domain.Playlist import ImageBase64, Playlist, PlaylistAuthor, PlaylistDescription, PlaylistFileName, PlaylistId, PlaylistInfo, PlaylistTitle
from Domain.Song import Song


# init settings
is_dev = os.environ['IS_DEV_BINARY'] == str(1)
dropbox_token = os.environ['DROPBOX_ACCESS_TOKEN']
dropbox_path = 'BSPlaylistManager-dev' if is_dev else 'BSPlaylistManager'


# definition
class Dropbox:
    # dropboxもapplicationserviceを作ってもいいかもしれない
    # 上の階層でやるべき処理がこちらで集約されている気がする。要見直し。

    def __init__(self):
        self.dbx = dropbox.Dropbox(dropbox_token)
        self.dpathInfoList = "/{}/PlaylistInfoList".format(dropbox_path)
        self.fpathInfoList = "{}/infoList.csv".format(self.dpathInfoList)
        self.dpathPlaylist = "/{}/Playlists".format(dropbox_path)

        # make playlist folder if the folder does not exists
        entryList = self._findPathList(self.dpathPlaylist)
        if len(entryList) == 0:
            self.dbx.files_create_folder_v2(self.dpathPlaylist)

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

        # read info list
        infoList = []
        try:
            with open(self.fpathInfoList) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    info = self._convertInfoListFromJson(row)
                    infoList += [info]
        except FileNotFoundError:
            self._createInfoList()
            return

        # if the file is empty file
        if len(infoList) == 0:
            self._createInfoList()
            return
        else:
            return infoList

    # 指定の文字列を含むフォルダ・ファイルパスの一覧を返す
    def _findPathList(self, keyword: str, entryList: list = list()) -> List[str]:
        res = self.dbx.files_list_folder("", recursive=True)
        entryList += [
            entry for entry in res.entries if (keyword in entry.path_display)]
        return entryList

    # プレイリスト情報一覧を新規作成する
    def _createInfoList(self):

        # make info list folder if the folder does not exists
        entryList = self._findPathList(self.dpathInfoList)
        raise Exception(len(entryList))
        if len(entryList) == 0:
            self.dbx.files_create_folder_v2(self.dpathInfoList)

        # create info list file
        fileList = self._findPathList(self.fpathInfoList)
        raise Exception(fileList)
        if len(fileList) == 0:
            with open(self.fpathInfoList, "x") as f:
                writer = csv.DictWriter(f, ["ID", "FileName", "Title"])
                writer.writeheader()

    # プレイリスト情報一覧を json 形式から変換する
    def _convertInfoListFromJson(self, infoListJson: dict) -> PlaylistInfo:

        # key exists check
        infoListKeys = ["ID", "FileName", "Title"]
        if set(infoListJson.keys()) != infoListKeys:
            raise Exception("プレイリスト情報一覧の読み込み中にエラーが発生したよ！")

        # get info
        playlistInfo = PlaylistInfo(
            playlistId=PlaylistId(infoListJson["ID"]),
            playlistFileName=PlaylistFileName(infoListJson["FileName"]),
            playlistTitle=PlaylistTitle(infoListJson["Title"])
        )
        return playlistInfo

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
    def registerInfo(self, playlistInfo: PlaylistInfo):

        # read info list
        infoList = self._readInfoList()

        # duplicated check for Id and FileName and Title
        if infoList is not None:
            if playlistInfo.playlistId in [info.playlistId for info in infoList]:
                raise Exception
            if playlistInfo.playlistFileName in [info.playlistFileName for info in infoList]:
                raise Exception
            if playlistInfo.playlistTitle in [info.playlistTitle for info in infoList]:
                raise Exception

        # convert info into dict
        infoDict = {
            "ID": playlistInfo.playlistId,
            "FileName": playlistInfo.playlistFileName,
            "Title": playlistInfo.playlistTitle
        }

        # register info
        try:
            with open(self.fpathInfoList, "a") as f:
                writer = csv.DictWriter(f, ["ID", "FileName", "Title"])
                writer.writerow(infoDict)
        except FileNotFoundError:
            self._createInfoList()

    # ----------------------------------

    def unregisterInfo(self, playlistInfo: PlaylistInfo, playlistFileName: PlaylistFileName = PlaylistFileName("infoList")):

        # read info list
        infoList = self._readInfoList()

        # unregister info
        infoList.remove(playlistInfo)

        # unregister info
        with open(self.fpathInfoList, "w") as f:
            writer = csv.DictWriter(f, ["ID", "FileName", "Title"])
            writer.writeheader()
            for info in infoList:
                infoDict = {
                    "ID": info.playlistId,
                    "FileName": info.playlistFileName,
                    "Title": info.playlistTitle
                }
                writer.writerow(infoDict)

    def deletePlaylist(self, playlistInfo: PlaylistInfo):

        # set file path
        filePath = "{}/{}.json".format(self.dpathPlaylist,
                                       playlistInfo.playlistFileName.playlistFileName)

        # delete playlist
        self.dbx.files_delete(filePath)

    # ----------------------------------

    def getSharedLink(self, playlistTitle: PlaylistTitle) -> str:

        # find info by title
        info = self.findInfoByTitle(playlistTitle)
        if info is None:
            raise Exception("指定のプレイリストが見つからないよ！")

        # set file path
        filePath = "{}/{}.json".format(self.dpathPlaylist,
                                       info.playlistFileName.playlistFileName)

        # get link
        links = self.dbx.sharing_list_shared_links(
            path=self.fpath, direct_only=True).links

        if links is not None:
            for link in links:
                return link.url.replace("dl=0", "dl=1")
            raise Exception("リンクの取得に失敗したよ！")
        else:
            return self._createSharedLink(filePath)

    def _createSharedLink(self, filePath: str) -> str:

        # create shared link
        setting = dropbox.sharing.SharedLinkSettings(
            requested_visibility=dropbox.sharing.RequestedVisibility.public)
        link = self.dbx.sharing_create_shared_link_with_settings(
            path=filePath, settings=setting)
        return link.url.replace("dl=0", "dl=1")

    # ----------------------------------

    # 指定のパスが存在するかどうかを返す
    def _fileExistsInfoList(self, filePath: str) -> bool:
        fileList = self._findPathList(filePath)
        return len(fileList) == 0

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
