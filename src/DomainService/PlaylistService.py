
# load modules
import inject
from src.Domain.Playlist import Playlist, PlaylistID, PlaylistKeyword
from src.Domain.Song import SongID
from src.Repository.Abstract.PlaylistRepository import IPlaylistRepository
from src.Repository.Abstract.SongRepository import ISongRepository


# definition
class PlaylistService:

    # instance fields
    songRepository: ISongRepository = inject.attr(ISongRepository)
    playlistRepository: IPlaylistRepository = inject.attr(IPlaylistRepository)

    # post init
    def __post_init__(self):

        # type check
        if not isinstance(self.songRepository, ISongRepository):
            raise Exception
        if not isinstance(self.playlistRepository, IPlaylistRepository):
            raise Exception

    # ------------------------

    def existsByID(self, playlistID: PlaylistID) -> bool:

        # find playlist by ID
        playlist = self.playlistRepository.findByID(playlistID)

        # judge
        exists = playlist is not None

        # return
        return exists

    def existsByKeyword(self, playlistKeyword: PlaylistKeyword) -> bool:

        # find playlistID by keyword
        playlistID = self.playlistRepository.findIDByKeyword(playlistKeyword)

        # judge
        exists = playlistID is not None

        # return
        return exists

    def hasTheSong(self, playlistID: PlaylistID, songID: SongID) -> bool:

        # find playlist by ID
        playlist = self.playlistRepository.findByID(playlistID)

        # judge
        exists = False
        if playlist is not None:
            if songID in playlist.songIDs:
                exists = True

        # return
        return exists

    # ------------------------

    # convert playlist to json
    def convert2Json(self, playlist: Playlist) -> dict:

        # get song hash
        songs = []
        for songID in playlist.songIDs:
            hash = self.songRepository.findHashByID(songID)
            songs.append({"hash", hash.hash})

        # set playlist
        playlistJson = {
            "playlistTitle": playlist.title,
            "playlistAuthor": playlist.author,
            "playlistDescription": playlist.description,
            "image": playlist.image,
            "songs": songs
        }

        # return
        return playlistJson
