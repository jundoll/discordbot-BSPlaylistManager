
# load modules
from typing import List, Tuple
import aiohttp
import inject
from src.Domain.Playlist import (Playlist, PlaylistAuthor, PlaylistDescription,
                                 PlaylistFileName, PlaylistID, PlaylistKeyword,
                                 PlaylistTitle, SearchKeyword)
from src.Domain.Song import SongHash, Url
from src.DomainService.PlaylistService import PlaylistService
from src.Factory.Abstract.ImageFactory import IImageFactory
from src.Factory.Abstract.SongFactory import ISongFactory
from src.Message.Error import OriginalException
from src.Message.Message import ExceptionMessages, Messages
from src.Repository.Abstract.PlaylistRepository import IPlaylistRepository
from src.Repository.Abstract.SongRepository import ISongRepository


# definition
class PlaylistApplicationService:

    # instance fields
    imageFactory: IImageFactory = inject.attr(IImageFactory)
    songFactory: ISongFactory = inject.attr(ISongFactory)
    songRepository: ISongRepository = inject.attr(ISongRepository)
    playlistRepository: IPlaylistRepository = inject.attr(IPlaylistRepository)

    # post init
    def __post__init__(self):

        # type check
        if not isinstance(self.songFactory, ISongFactory):
            raise Exception

    # ---------------------

    # キーワードに一致するプレイリストを検索して、曲を追加する
    def addSong(self, arg_keyword: str, arg_url: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception
        if not isinstance(arg_url, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)
        url = Url(arg_url)

        # キーワードに一致するプレイリストIDを検索する
        playlistID = self.playlistRepository.findIDByKeyword(keyword)
        if playlistID is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # URLから曲情報を取得する
        songs = self.songFactory.generateByUrl(url)

        # 1曲の場合
        if len(songs) == 1:
            for song in songs:

                # 曲情報を新規登録または更新する
                self.songRepository.upsert(song)

                # プレイリストに曲情報が登録されているかどうかを確認する
                self.playlistService = PlaylistService()
                exists = self.playlistService.hasTheSong(
                    playlistID, song.songID)

                # 未登録であれば登録する
                if exists:
                    raise OriginalException(
                        ExceptionMessages.alreadyExistsSongExceptionMessage())
                else:
                    self.playlistRepository.insertSong(playlistID, song.songID)
                    raise OriginalException(Messages.addSongMessage())

        # 複数曲ある場合
        else:
            numberOfAdded = 0
            for song in songs:

                # 曲情報を新規登録または更新する
                self.songRepository.upsert(song)

                # プレイリストに曲情報が登録されているかどうかを確認する
                self.playlistService = PlaylistService()
                exists = self.playlistService.hasTheSong(
                    playlistID, song.songID)

                # 未登録であれば登録する
                if not exists:
                    self.playlistRepository.insertSong(playlistID, song.songID)
                    numberOfAdded += 1

            # message
            if numberOfAdded == 0:
                raise OriginalException(ExceptionMessages.nonAddSongMessage())
            else:
                raise OriginalException(
                    Messages.addSongsMessage(numberOfAdded))

    def deleteSong(self, arg_keyword: str, arg_url: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception
        if not isinstance(arg_url, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)
        url = Url(arg_url)

        # キーワードに一致するプレイリストIDを検索する
        playlistID = self.playlistRepository.findIDByKeyword(keyword)
        if playlistID is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # URLから曲情報を取得する
        songs = self.songFactory.generateByUrl(url)

        # 1曲の場合
        if len(songs) == 1:
            for song in songs:

                # プレイリストに曲情報が登録されているかどうかを確認する
                self.playlistService = PlaylistService()
                exists = self.playlistService.hasTheSong(
                    playlistID, song.songID)

                # 登録済みであれば削除する
                if exists:
                    self.playlistRepository.deleteSong(playlistID, song.songID)
                    self.songRepository.delete(song.songID)
                    raise OriginalException(Messages.deleteSongMessage())
                else:
                    raise OriginalException(
                        ExceptionMessages.songNotFoundExceptionMessage())

        # 複数曲ある場合
        else:
            numberOfDeleted = 0
            for song in songs:

                # プレイリストに曲情報が登録されているかどうかを確認する
                self.playlistService = PlaylistService()
                exists = self.playlistService.hasTheSong(
                    playlistID, song.songID)

                # 登録済みであれば削除する
                if exists:
                    self.playlistRepository.deleteSong(playlistID, song.songID)
                    self.songRepository.delete(song.songID)
                    numberOfDeleted += 1

            # message
            if numberOfDeleted == 0:
                raise OriginalException(
                    ExceptionMessages.nonDeleteSongMessage())
            else:
                raise OriginalException(
                    Messages.deleteSongsMessage(numberOfDeleted))

    # ---------------------

    # 空のプレイリストを新規作成する
    def addPlaylist(self, arg_keyword: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)

        # キーワードに一致するプレイリストが存在するかどうかを確認する
        self.playlistService = PlaylistService()
        exists = self.playlistService.existsByKeyword(keyword)

        if exists:
            # return message
            raise OriginalException(
                ExceptionMessages.alreadyExistsPlaylistExceptionMessage())

        # set new playlist
        playlist = Playlist(
            playlistID=PlaylistID(),
            fileName=PlaylistFileName(keyword.keyword),
            keyword=PlaylistKeyword(keyword.keyword),
            title=PlaylistTitle(keyword.keyword),
            author=PlaylistAuthor("discordbot-BSPlaylistManager"),
            description=PlaylistDescription(
                "This is generated by discordbot-BSPlaylistManager."),
            image=self.imageFactory.generateByKeyword(keyword),
            songIDs=[]
        )

        # insert playlist
        self.playlistRepository.insertPlaylist(playlist)

        # return message
        raise OriginalException(Messages.addPlaylistMessage(keyword.keyword))

    # 既存のプレイリストを登録する
    async def registerPlaylist(self, arg_keyword: str, arg_url: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception
        if not isinstance(arg_url, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)

        # キーワードに一致するプレイリストが存在するかどうかを確認する
        self.playlistService = PlaylistService()
        exists = self.playlistService.existsByKeyword(keyword)

        if exists:
            # return message
            raise OriginalException(
                ExceptionMessages.alreadyExistsPlaylistExceptionMessage())

        # get playlist json
        async with aiohttp.ClientSession() as session:
            async with session.get(arg_url) as r:
                if r.status == 200:
                    playlistJson = await r.json()
                else:
                    return

        # make songID list
        songIDs = []
        for songJson in playlistJson["songs"]:
            # get song
            song = self.songRepository.findByHash(SongHash(songJson["hash"]))
            if song is None:
                song = self.songFactory.generateByHash(
                    SongHash(songJson["hash"]))
                self.songRepository.upsert(song)

            # append
            songIDs.append(song.songID)

        # set new playlist
        playlist = Playlist(
            playlistID=PlaylistID(),
            fileName=PlaylistFileName(keyword.keyword),
            keyword=PlaylistKeyword(keyword.keyword),
            title=PlaylistTitle(keyword.keyword),
            author=PlaylistAuthor("discordbot-BSPlaylistManager"),
            description=PlaylistDescription(
                "This is generated by discordbot-BSPlaylistManager."),
            image=self.imageFactory.generateByKeyword(
                PlaylistKeyword(arg_keyword)),
            songIDs=songIDs
        )

        # insert playlist
        self.playlistRepository.insertPlaylist(playlist)

        # return message
        raise OriginalException(
            Messages.registerPlaylistMessage(keyword.keyword))

    # ---------------------

    # プレイリストを削除する

    def deletePlaylist(self, arg_keyword: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)

        # キーワードに一致するプレイリストIDを検索する
        playlistID = self.playlistRepository.findIDByKeyword(keyword)
        if playlistID is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # プレイリストを削除する
        self.playlistRepository.deletePlaylist(playlistID)

        # return message
        raise OriginalException(Messages.deletePlaylistMessage())

    # プレイリストを復元する
    def restorePlaylist(self, arg_keyword: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)

        # キーワードに一致するプレイリストIDを検索する
        playlistID = self.playlistRepository.findIDByKeyword(
            keyword, isDeleted=True)
        if playlistID is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # プレイリストを復元する
        self.playlistRepository.restorePlaylist(playlistID)

        # return message
        raise OriginalException(Messages.restorePlaylistMessage())

    # ---------------------

    # ファイル名を更新する
    def updateFileName(self, arg_keyword: str, arg_filename: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception
        if not isinstance(arg_filename, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)
        filename = PlaylistFileName(arg_filename)

        # キーワードからプレイリストを検索する
        playlist = self.playlistRepository.findByKeyword(keyword)
        if playlist is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # 更新したプレイリスト情報を用意する
        playlist.fileName = filename

        # プレイリスト情報を更新する
        self.playlistRepository.update(playlist)

        # return message
        raise OriginalException(
            Messages.updatePlaylistInfoMessage())

    # キーワードを更新する
    def updateKeyword(self, arg_trg_keyword: str, arg_new_keyword: str):

        # type check
        if not isinstance(arg_trg_keyword, str):
            raise Exception
        if not isinstance(arg_new_keyword, str):
            raise Exception

        # set instance
        trg_keyword = PlaylistKeyword(arg_trg_keyword)
        new_keyword = PlaylistKeyword(arg_new_keyword)

        # 更新前キーワードからプレイリストを検索する
        playlist = self.playlistRepository.findByKeyword(trg_keyword)
        if playlist is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # 更新後キーワードからプレイリストを検索する
        playlistSameKeyword = self.playlistRepository.findByKeyword(
            new_keyword)
        if playlistSameKeyword is not None:
            raise OriginalException(
                ExceptionMessages.alreadyExistsPlaylistExceptionMessage())

        # 更新したプレイリスト情報を用意する
        playlist.keyword = new_keyword

        # プレイリスト情報を更新する
        self.playlistRepository.update(playlist)

        # return message
        raise OriginalException(
            Messages.updatePlaylistKeywordInfoMessage(playlist.keyword.keyword))

    # タイトルを更新する
    def updateTitle(self, arg_keyword: str, arg_title: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception
        if not isinstance(arg_title, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)
        title = PlaylistTitle(arg_title)

        # キーワードからプレイリストを検索する
        playlist = self.playlistRepository.findByKeyword(keyword)
        if playlist is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # 更新したプレイリスト情報を用意する
        playlist.title = title

        # プレイリスト情報を更新する
        self.playlistRepository.update(playlist)

        # return message
        raise OriginalException(
            Messages.updatePlaylistInfoMessage())

    # 作成者を更新する
    def updateAuthor(self, arg_keyword: str, arg_author: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception
        if not isinstance(arg_author, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)
        author = PlaylistAuthor(arg_author)

        # キーワードからプレイリストを検索する
        playlist = self.playlistRepository.findByKeyword(keyword)
        if playlist is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # 更新したプレイリスト情報を用意する
        playlist.author = author

        # プレイリスト情報を更新する
        self.playlistRepository.update(playlist)

        # return message
        raise OriginalException(
            Messages.updatePlaylistInfoMessage())

    # 説明を更新する
    def updateDescription(self, arg_keyword: str, arg_description: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception
        if not isinstance(arg_description, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)
        description = PlaylistDescription(arg_description)

        # キーワードからプレイリストを検索する
        playlist = self.playlistRepository.findByKeyword(keyword)
        if playlist is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # 更新したプレイリスト情報を用意する
        playlist.description = description

        # プレイリスト情報を更新する
        self.playlistRepository.update(playlist)

        # return message
        raise OriginalException(
            Messages.updatePlaylistInfoMessage())

    # 画像を更新する
    async def updateImage(self, arg_keyword: str, arg_url: str):

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception
        if not isinstance(arg_url, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)
        image = await self.imageFactory.convertByImageFile(arg_url)

        # キーワードからプレイリストを検索する
        playlist = self.playlistRepository.findByKeyword(keyword)
        if playlist is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # 更新したプレイリスト情報を用意する
        playlist.image = image

        # プレイリスト情報を更新する
        self.playlistRepository.update(playlist)

        # return message
        raise OriginalException(
            Messages.updatePlaylistInfoMessage())

    # ---------------------

    # プレイリストをダウンロードする
    def download(self, arg_keyword: str) -> Tuple[str, dict, Playlist]:

        # type check
        if not isinstance(arg_keyword, str):
            raise Exception

        # set instance
        keyword = PlaylistKeyword(arg_keyword)

        # キーワードからプレイリストを検索する
        playlist = self.playlistRepository.findByKeyword(keyword)
        if playlist is None:
            raise OriginalException(
                ExceptionMessages.playlistOfKeywordNotFoundExceptionMessage())

        # 更新したプレイリスト情報を用意する
        playlistService = PlaylistService()
        playlistJson = playlistService.convert2Json(playlist)

        # return message
        return (Messages.downloadPlaylistMessage(), playlistJson, playlist)

    # ---------------------

    # プレイリストをあいまい検索する
    def search(self, search_keyword: str) -> Tuple[str, List[Playlist]]:

        # type check
        if not isinstance(search_keyword, str):
            raise Exception

        # set instance
        searchKeyword = SearchKeyword(search_keyword)

        # キーワードからプレイリストを検索する
        playlists = self.playlistRepository.fuzzyFindByKeyword(searchKeyword)
        if playlists is None:
            raise OriginalException(
                ExceptionMessages.playlistOfSearchKeywordNotFoundExceptionMessage())
        elif len(playlists) == 0:
            raise OriginalException(
                ExceptionMessages.playlistOfSearchKeywordNotFoundExceptionMessage())

        # return message
        return (Messages.foundPlaylistMessage(), playlists)

    # ---------------------
