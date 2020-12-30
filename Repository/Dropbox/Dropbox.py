
# load modules
import json
import os
from typing import List, Union
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
        self.fpathInfoList = "{}/infoList.json".format(self.dpathInfoList)
        self.dpathPlaylist = "/{}/Playlists".format(dropbox_path)

    # ---------------------

    # タイトルからプレイリスト情報を読み込む
    def readInfoByTitle(self, playlistTitle: PlaylistTitle) -> Union[PlaylistInfo, None]:

        # プレイリスト情報一覧を読み込む
        infoList = self.readInfoListByTitle()

        # タイトルからプレイリスト情報を取得する
        for info in infoList:
            if info.playlistTitle == playlistTitle:
                return info

    # ---------------------

    # プレイリスト情報一覧を読み込む
    def readInfoListByTitle(self) -> Union[List[PlaylistInfo], None]:

        # プレイリスト情報一覧を json 形式で読み込む
        infoListJson = self._readJsonFile(self.fpathInfoList)
        if infoListJson is None:
            return

        # プレイリスト情報一覧を json 形式から変換する
        infoList = self._convertInfoListFromJson(infoListJson)

        # return
        return infoList

    # json 形式のファイルを読み込む
    def _readJsonFile(self, filePath: str) -> Union[dict, None]:

        # exist check
        pathList = self._findPathList(filePath)
        if len(pathList) == 0:
            return

        # json 形式のファイルを取得する
        try:
            metadata, res = self.dbx.files_download(filePath)
        except Exception as e:
            print(e)
            raise Exception("ファイルの取得に失敗したよ！")

        # json 形式のファイルを読み込む
        readJson = json.loads(res.content)
        return readJson

    # 指定の文字列を含むフォルダ・ファイルパスの一覧を返す
    def _findPathList(self, keyword: str) -> List[str]:

        # 指定の文字列を含むフォルダ・ファイルパスの一覧を取得する
        res = self.dbx.files_list_folder("", recursive=True)
        entryList = [] + \
            [entry.path_lower for entry in res.entries if (
                keyword in entry.path_display)]

        # return
        return entryList

    # プレイリスト情報一覧を json 形式から変換する
    def _convertInfoListFromJson(self, infoListJson: dict) -> List[PlaylistInfo]:

        # プレイリスト情報一覧に特定のキーが存在するかどうかのチェック
        infoListKeys = ["infoList"]
        if set(infoListJson.keys()) != set(infoListKeys):
            raise Exception("プレイリスト情報一覧の読み込み中にエラーが発生したよ！")

        # 取得した元のプレイリスト情報一覧を変換する
        infoList = []
        for infoJson in infoListJson["infoList"]:

            # プレイリスト情報に特定のキーが存在するかどうかのチェック
            infoKeys = ["ID", "FileName", "Title"]
            if set(infoJson.keys()) != set(infoKeys):
                raise Exception("プレイリスト情報の読み込み中にエラーが発生したよ！")

            # 取得した元のプレイリスト情報を変換する
            info = PlaylistInfo(
                playlistId=PlaylistId(infoJson["ID"]),
                playlistFileName=PlaylistFileName(infoJson["FileName"]),
                playlistTitle=PlaylistTitle(infoJson["Title"])
            )

            # プレイリスト情報をリストに追加する
            infoList += [info]

        # return
        return infoList

    # ----------------------------------

    # プレイリスト情報を保存する
    def saveInfoList(self, playlistInfoList: List[PlaylistInfo]):

        # 格納フォルダがなければ作成する
        entryList = self._findPathList(self.dpathInfoList)
        if len(entryList) == 0:
            self.dbx.files_create_folder_v2(self.dpathInfoList)

        # プレイリスト情報一覧を json 形式に変換する
        playlistInfoListJson = {"infoList": []}
        for info in playlistInfoList:
            infoDict = {
                "ID": info.playlistId,
                "FileName": info.playlistFileName,
                "Title": info.playlistTitle
            }
            playlistInfoListJson["infoList"].append(infoDict)

        # json 形式のプレイリスト情報一覧を保存する
        self._saveJsonFile(playlistInfoListJson, self.fpathInfoList)

    # json 形式のファイルを保存する
    def _saveJsonFile(self, jsonData: dict, filePath: str):

        # dump する
        jsonDataBytes = bytes(json.dumps(jsonData,
                                         separators=(',', ':'), ensure_ascii=False), encoding="utf-8")

        # json 形式のファイルを保存する
        try:
            self.dbx.files_upload(jsonDataBytes, filePath,
                                  mode=dropbox.files.WriteMode.overwrite)
        except Exception:
            raise Exception("ファイルの保存に失敗したよ！")

    # ----------------------------------

    # プレイリストを読み込む
    def readPlaylist(self, playlistInfo: PlaylistInfo) -> Union[Playlist, None]:

        # ファイルパスを指定する
        filePath = "{}/{}.json".format(self.dpathPlaylist,
                                       playlistInfo.playlistFileName.playlistFileName)

        # プレイリストを json 形式で読み込む
        playlistJson = self._readJsonFile(filePath)
        if playlistJson is None:
            return

        # プレイリストを json 形式から変換する
        playlist = self._convertPlaylistFromJson(playlistJson, playlistInfo)
        return playlist

    # プレイリストを json 形式から変換する
    def _convertPlaylistFromJson(self, playlistJson: dict, playlistInfo: PlaylistInfo) -> Union[Playlist, None]:

        # プレイリストに特定のキーが存在するかどうかのチェック
        playlistKeys = ["playlistTitle", "playlistAuthor",
                        "playlistDescription", "image", "songs"]
        if set(playlistJson.keys()) != set(playlistKeys):
            raise Exception("プレイリストの読み込み中にエラーが発生したよ！")

        # 取得した元のプレイリストを変換する
        playlist = Playlist(
            playlistInfo=playlistInfo,
            playlistTitle=playlistInfo.playlistTitle,
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
    def savePlaylist(self, playlist: Playlist):

        # ファイルパスを指定する
        filePath = "{}/{}.json".format(self.dpathPlaylist,
                                       playlist.playlistInfo.playlistFileName.playlistFileName)

        # 格納フォルダがなければ作成する
        entryList = self._findPathList(self.dpathPlaylist)
        if len(entryList) == 0:
            self.dbx.files_create_folder_v2(self.dpathPlaylist)

        # プレイリストを json 形式に変換する
        playlistJson = {
            "playlistTitle": playlist.playlistTitle.playlistTitle,
            "playlistAuthor": playlist.playlistAuthor.playlistAuthor,
            "playlistDescription": playlist.playlistDescription.playlistDescription,
            "image": playlist.image.image,
            "songs": [song.convertJson() for song in playlist.songs]
        }

        # json 形式のプレイリストを保存する
        self._saveJsonFile(playlistJson, filePath)

    # ----------------------------------

    # タイトルからプレイリストを削除する
    def deletePlaylist(self, playlistTitle: PlaylistTitle):

        # タイトルからプレイリスト情報を取得する
        playlistInfo = self.readInfoByTitle(playlistTitle)
        if playlistInfo is None:
            raise Exception("指定のプレイリストが見つからないよ！")
            # エラーケース
            # ・プレイリスト情報一覧が見つからない
            # ・プレイリスト情報一覧に一致するタイトルが見つからない

        # ファイルパスを指定する
        filePath = "{}/{}.json".format(self.dpathPlaylist,
                                       playlistInfo.playlistFileName.playlistFileName)

        # 格納フォルダがなければ作成する
        entryList = self._findPathList(self.dpathPlaylist)
        if len(entryList) == 0:
            self.dbx.files_create_folder_v2(self.dpathPlaylist)
            return

        # プレイリストを削除する
        try:
            self.dbx.files_delete(filePath)
        except Exception:
            raise Exception("プレイリストの削除に失敗したよ！")

    # ----------------------------------

    # タイトルからプレイリストのダウンロードURLを取得する
    def getSharedLink(self, playlistTitle: PlaylistTitle) -> Union[str, None]:

        # タイトルからプレイリスト情報を取得する
        playlistInfo = self.readInfoByTitle(playlistTitle)
        if playlistInfo is None:
            raise Exception("指定のプレイリストが見つからないよ！")
            # エラーケース
            # ・プレイリスト情報一覧が見つからない
            # ・プレイリスト情報一覧に一致するタイトルが見つからない

        # ファイルパスを指定する
        filePath = "{}/{}.json".format(self.dpathPlaylist,
                                       playlistInfo.playlistFileName.playlistFileName)

        # 共有リンクを取得する
        links = self.dbx.sharing_list_shared_links(
            path=filePath, direct_only=True).links

        if links is None:
            # 共有リンクを発行する
            links = [self._createSharedLink(filePath)]

        if len(links) == 0:
            raise Exception("リンクの取得に失敗したよ！")
        else:
            for link in links:
                return link.url.replace("dl=0", "dl=1")

    # 共有リンクを発行する
    def _createSharedLink(self, filePath: str) -> str:

        # 共有リンクを発行する
        setting = dropbox.sharing.SharedLinkSettings(
            requested_visibility=dropbox.sharing.RequestedVisibility.public)
        link = self.dbx.sharing_create_shared_link_with_settings(
            path=filePath, settings=setting)
        return link
