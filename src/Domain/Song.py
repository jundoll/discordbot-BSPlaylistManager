
# load modules
from dataclasses import dataclass


# definition value object
@dataclass(frozen=True)
class Url:

    url: str

    def __post_init__(self):

        # type check
        if not isinstance(self.url, str):
            raise Exception

        # empty check
        if len(self.url) == 0:
            raise Exception


@dataclass(frozen=True)
class SongID:

    ID: str

    def __post_init__(self):

        # type check
        if not isinstance(self.ID, str):
            raise Exception

        # empty check
        if len(self.ID) == 0:
            raise Exception


@dataclass(frozen=True)
class SongHash:

    hash: str

    def __post_init__(self):

        # type check
        if not isinstance(self.hash, str):
            raise Exception

        # empty check
        if len(self.hash) == 0:
            raise Exception


# definition entity
@dataclass(frozen=True)
class Song:

    songID: SongID
    hash: SongHash

    def __post_init__(self):

        # type check
        if not isinstance(self.songID, SongID):
            raise Exception
        if not isinstance(self.hash, SongHash):
            raise Exception
