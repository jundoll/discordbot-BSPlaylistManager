
# load modules
from dataclasses import dataclass
from typing import Dict


# definition
@dataclass(frozen=True)
class Song:

    hash: str

    def __post_init__(self):

        # type check
        if not isinstance(self.hash, str):
            raise Exception

        # empty check
        if len(self.hash) == 0:
            raise Exception

    def __hash__(self):
        return hash(str(self))

    def convertJson(self) -> Dict[str]:
        val = dict(hash=self.hash)
        return val
