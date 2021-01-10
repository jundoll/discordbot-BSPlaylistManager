
# messages
from src.Domain.Playlist import PlaylistKeyword


class Messages:

    @classmethod
    def addSongMessage(cls) -> str:
        return "プレイリストに曲を追加したよ！"

    @classmethod
    def addPlaylistMessage(cls, keyword: PlaylistKeyword) -> str:
        return "プレイリストを作成したよ！キーワード「" + keyword.keyword + "」を使って曲を追加してね！"

    @classmethod
    def registerPlaylistMessage(cls, keyword: PlaylistKeyword) -> str:
        return "プレイリストを登録したよ！キーワード「" + keyword.keyword + "」を使って曲を追加してね！"

    @classmethod
    def deleteSongMessage(cls) -> str:
        return "プレイリストから曲を削除したよ！"

    @classmethod
    def deletePlaylistMessage(cls) -> str:
        return "プレイリストを削除したよ！まだ今ならrestoreコマンドで復元できるよ！"

    @classmethod
    def restorePlaylistMessage(cls) -> str:
        return "プレイリストを復元したよ！"

    @classmethod
    def updatePlaylistInfoMessage(cls, keyword: PlaylistKeyword) -> str:
        return "プレイリスト情報を更新したよ！キーワード「" + keyword.keyword + "」を使って曲を追加してね！"

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
        return "APIの取得に失敗したよ！"

    @classmethod
    def GetURLForMapperErrorMessage(cls) -> str:
        return "mapper は https://beatsaver.com から検索してね！"

    @classmethod
    def DownloadDropboxFileErrorMessage(cls) -> str:
        return "ファイルの取得に失敗したよ！"

    @classmethod
    def uniquePlaylistPlaylistIDErrorMessage(cls) -> str:
        return "[UNIQUE制約エラー] playlist.playlistID"

    @classmethod
    def uniquePlaylistKeywordErrorMessage(cls) -> str:
        return "[UNIQUE制約エラー] playlist.keyword"
