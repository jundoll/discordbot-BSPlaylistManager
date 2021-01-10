
# load modules
import json
import os
from typing import List, Union
import dropbox
from src.Message.Error import OriginalException
from src.Message.Message import ErrorMessages


# definition
class DropboxHandler:

    IS_DEV = os.environ['IS_DEV_BINARY'] == str(1)
    DROPBOX_TOKEN = os.environ['DROPBOX_ACCESS_TOKEN']
    DROPBOX_PATH = 'BSPlaylistManager-dev' if IS_DEV else 'BSPlaylistManager'
    SONG_DB_PATH = "/{}/song.json".format(DROPBOX_PATH)
    PLAYLIST_DB_PATH = "/{}/playlist.json".format(DROPBOX_PATH)
    PLAYLIST_DETAIL_DB_PATH = "/{}/playlistJson.json".format(DROPBOX_PATH)

    def __init__(self):
        self.dbx = dropbox.Dropbox(self.DROPBOX_TOKEN)

    # ---------------------

    # 指定の文字列を含むフォルダ・ファイルパスの一覧を返す
    def findPathList(self, keyword: str) -> List[str]:

        # 指定の文字列を含むフォルダ・ファイルパスの一覧を取得する
        res = self.dbx.files_list_folder("", recursive=True)
        pathList = []
        for entry in res.entries:
            if keyword in entry.path_display:
                pathList.append(entry.path_lower)

        # return
        return pathList

    # json 形式のファイルを読み込む
    def readJsonFile(self, filePath: str) -> Union[dict, None]:

        # exist check
        pathList = self.findPathList(filePath)
        if len(pathList) == 0:
            return

        # json 形式のファイルを取得する
        try:
            metadata, res = self.dbx.files_download(filePath)
        except Exception as e:
            raise OriginalException(
                ErrorMessages.DownloadDropboxFileErrorMessage())

        # json 形式のファイルを読み込む
        readJson = json.loads(res.content)
        return readJson

    # json 形式のファイルを保存する
    def saveJsonFile(self, jsonData: dict, filePath: str):

        # dump する
        jsonDataBytes = bytes(json.dumps(jsonData, separators=(
            ',', ':'), ensure_ascii=False), encoding="utf-8")

        # json 形式のファイルを保存する
        try:
            self.dbx.files_upload(jsonDataBytes, filePath,
                                  mode=dropbox.files.WriteMode.overwrite)
            raise OriginalException(
                ErrorMessages.DownloadDropboxFileErrorMessage())
