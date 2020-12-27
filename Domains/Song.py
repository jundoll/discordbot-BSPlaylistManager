
# load modules
from typing import List
from dataclasses import dataclass, field


# init settings

# definition
@dataclass(frozen=True)
class Song:

    hash: str

    def __post_init__(self):
        if self.hash == "":
            raise Exception

    def parseJson(self):
        val = dict(hash=self.hash)
        return val

@dataclass
class SongList:

    songList: List[Song] = field(default=list())

    def add(self, song:Song):
        self.songList += [song]
        self.songList = [dict(song) for song in {tuple(song0.items()) for song0 in self.songList}]

    def delete(self, song:Song):
        self.songList -= [song]

    def parseJson(self):
        val = [ song.parseJson() for song in self.songList ]
        return val


