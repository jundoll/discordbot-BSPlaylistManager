
# load modules
import uuid
from dataclasses import dataclass, field
from typing import List
from src.Domain.Song import SongID
from src.Message.Error import OriginalException
from src.Message.Message import ErrorMessages


# definition
@dataclass(frozen=True)
class PlaylistID:

    ID: str = field(default=str(uuid.uuid4()))

    def __post_init__(self):

        # type check
        if not isinstance(self.ID, str):
            raise Exception

        # empty check
        if len(self.ID) == 0:
            raise Exception


@ dataclass(frozen=True)
class PlaylistFileName:

    filename: str  # 「.json」は含めない

    def __post_init__(self):

        # type check
        if not isinstance(self.filename, str):
            raise Exception

        # empty check
        if len(self.filename) == 0:
            raise Exception


@ dataclass(frozen=True)
class PlaylistKeyword:

    keyword: str

    def __post_init__(self):

        # type check
        if not isinstance(self.keyword, str):
            raise Exception

        # empty check
        if len(self.keyword) == 0:
            raise OriginalException(ErrorMessages.EmptyErrorMessage())


@ dataclass(frozen=True)
class PlaylistTitle:

    title: str

    def __post_init__(self):

        # type check
        if not isinstance(self.title, str):
            raise Exception

        # empty check
        if len(self.title) == 0:
            raise Exception


@ dataclass(frozen=True)
class PlaylistAuthor:

    author: str

    def __post_init__(self):

        # type check
        if not isinstance(self.author, str):
            raise Exception


@ dataclass(frozen=True)
class PlaylistDescription:

    description: str

    def __post_init__(self):

        # type check
        if not isinstance(self.description, str):
            raise Exception


@ dataclass(frozen=True)
class ImageBase64:

    image: str
    # 指定画像にプレイリスト名を埋めるとかありかも

    def __post_init__(self):

        # type check
        if not isinstance(self.image, str):
            raise Exception


@ dataclass(frozen=True)
class SearchKeyword:

    searchKeyword: str

    def __post_init__(self):

        # type check
        if not isinstance(self.searchKeyword, str):
            raise Exception

        # empty check
        if len(self.searchKeyword) == 0:
            raise OriginalException(ErrorMessages.EmptyErrorMessage())


@ dataclass
class Playlist:

    playlistID: PlaylistID
    fileName: PlaylistFileName
    keyword: PlaylistKeyword
    title: PlaylistTitle
    author: PlaylistAuthor
    description: PlaylistDescription
    image: ImageBase64
    songIDs: List[SongID]

    def __post_init__(self):

        # type check
        if not isinstance(self.playlistID, PlaylistID):
            raise Exception
        if not isinstance(self.fileName, PlaylistFileName):
            raise Exception
        if not isinstance(self.keyword, PlaylistKeyword):
            raise Exception
        if not isinstance(self.title, PlaylistTitle):
            raise Exception
        if not isinstance(self.author, PlaylistAuthor):
            raise Exception
        if not isinstance(self.description, PlaylistDescription):
            raise Exception
        if not isinstance(self.image, ImageBase64):
            raise Exception
        if not isinstance(self.songIDs, list):
            raise Exception
