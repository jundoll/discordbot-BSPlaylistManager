
# load modules
from typing import Dict, List
from dataclasses import dataclass


# init settings

# definition
@dataclass
class Song:

    hash: str


@dataclass
class SongList:

    songs: List[Dict[Song]]
