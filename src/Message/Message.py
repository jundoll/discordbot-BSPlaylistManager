
# messages


class Messages:

    @classmethod
    def addSongMessage(cls) -> str:
        return "プレイリストに曲を追加したよ！"

    @classmethod
    def addSongsMessage(cls, num: int) -> str:
        return "プレイリストに" + str(num) + "曲追加したよ！"

    @classmethod
    def addPlaylistMessage(cls, keyword: str) -> str:
        return "プレイリストを作成したよ！キーワード「" + keyword + "」を使って指定してね！"

    @classmethod
    def registerPlaylistMessage(cls, keyword: str) -> str:
        return "プレイリストを登録したよ！キーワード「" + keyword + "」を使って指定してね！"

    @classmethod
    def deleteSongMessage(cls) -> str:
        return "プレイリストから曲を削除したよ！"

    @classmethod
    def deleteSongsMessage(cls, num: int) -> str:
        return "プレイリストから" + str(num) + "曲削除したよ！"

    @classmethod
    def deletePlaylistMessage(cls) -> str:
        return "プレイリストを削除したよ！まだ今ならrestoreコマンドで復元できるよ！"

    @classmethod
    def restorePlaylistMessage(cls) -> str:
        return "プレイリストを復元したよ！"

    @classmethod
    def updatePlaylistKeywordInfoMessage(cls, keyword: str) -> str:
        return "プレイリスト情報を更新したよ！キーワード「" + keyword + "」を使って指定してね！"

    @classmethod
    def updatePlaylistInfoMessage(cls) -> str:
        return "プレイリスト情報を更新したよ！"

    @classmethod
    def downloadPlaylistMessage(cls) -> str:
        return "お望みのプレイリストだよ！"

    @classmethod
    def foundPlaylistMessage(cls) -> str:
        return "一致したプレイリストだよ！"


class ExceptionMessages:

    @classmethod
    def playlistOfKeywordNotFoundExceptionMessage(cls) -> str:
        return "そのキーワードのプレイリストはないよ！"

    @classmethod
    def alreadyExistsSongExceptionMessage(cls) -> str:
        return "その曲はもう追加済みだよ！"

    @classmethod
    def nonAddSongMessage(cls) -> str:
        return "追加する曲は無かったよ！"

    @classmethod
    def nonDeleteSongMessage(cls) -> str:
        return "削除する曲は無かったよ！"

    @classmethod
    def alreadyExistsPlaylistExceptionMessage(cls) -> str:
        return "そのキーワードのプレイリストはもうあるよ！違うキーワードで指定してね！"

    @classmethod
    def songNotFoundExceptionMessage(cls) -> str:
        return "その曲は登録されてないよ！"

    @classmethod
    def playlistOfSearchKeywordNotFoundExceptionMessage(cls) -> str:
        return "そのキーワードのプレイリストは見つからなかったよ！ワイルドカード(*)を使ってみてね！"


class ErrorMessages:

    @classmethod
    def EmptyErrorMessage(cls) -> str:
        return "１文字以上で指定してね！"

    @classmethod
    def APIErrorMessage(cls) -> str:
        return "APIの実行に失敗したよ！"

    @classmethod
    def GetURLForMapperErrorMessage(cls) -> str:
        return "Mapper は https://beatsaver.com から検索して Mapper のページを指定してね！"

    @classmethod
    def InvalidURLErrorMessage(cls) -> str:
        return "曲は https://beatsaver.com か https://bsaber.com からを検索して曲のページを指定してね！\nMapperは https://beatsaver.com からを検索して Mapper のページを指定してね！"

    @classmethod
    def DownloadDropboxFileErrorMessage(cls) -> str:
        return "ファイルの取得に失敗したよ！"

    @classmethod
    def DownloadImageFileErrorMessage(cls) -> str:
        return "ファイルの取得に失敗したよ！"

    @classmethod
    def uniquePlaylistPlaylistIDErrorMessage(cls) -> str:
        return "[UNIQUE制約エラー] playlist.playlistID"

    @classmethod
    def uniquePlaylistKeywordErrorMessage(cls) -> str:
        return "[UNIQUE制約エラー] playlist.keyword"
