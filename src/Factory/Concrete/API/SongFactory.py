
# load modules
import json
import re
from typing import List
from urllib import request
from src.Domain.Song import Song, SongHash, SongID, Url
from src.Factory.Abstract.SongFactory import ISongFactory
from src.Message.Error import OriginalException
from src.Message.Message import ErrorMessages


# constant value
BEATSAVER_API_MAP_BY_KEY = "https://beatsaver.com/api/maps/detail/"
BEATSAVER_API_MAP_BY_HASH = "https://beatsaver.com/api/maps/by-hash/"
BEATSAVER_API_MAPPER = "https://beatsaver.com/api/maps/uploader/"
USER_AGENT = "discordbot-BSPlaylistManager/1.0.0"
BEATSAVER_RE_URL_MAP = "^https://beatsaver.com/beatmap/[0-9a-fA-F]+/?$"
BEATSAVER_RE_URL_MAPPER = "^https://beatsaver.com/uploader/[0-9a-fA-F]+/?$"
BEASTSABER_RE_URL_MAP = "^https://bsaber.com/songs/[0-9a-fA-F]+/?$"
BEASTSABER_RE_URL_MAPPER = "^https://bsaber.com/members/[0-9a-fA-F]+/?$"


# definition
class SongFactory(ISongFactory):

    # URLからSongインスタンスのリストを生成する
    def generateByUrl(self, url: Url) -> List[Song]:

        # prepare return value
        songs = []

        # beat saver (map)
        if re.search(BEATSAVER_RE_URL_MAP, url.url) is not None:

            # extract key
            songKey = url.url.split('/')[4]

            # set request
            requestUrl = BEATSAVER_API_MAP_BY_KEY + "/" + songKey
            headers = {"User-Agent": USER_AGENT}
            req = request.Request(requestUrl, headers=headers)

            # send request
            try:
                response = request.urlopen(req)
                responseJson = json.load(response)
            except Exception:
                raise OriginalException(ErrorMessages.APIErrorMessage())

            # generate Song instance
            song = Song(
                songID=SongID(songKey),
                hash=SongHash(responseJson["hash"])
            )
            songs.append(song)

        # beat saver (mapper)
        elif re.search(BEATSAVER_RE_URL_MAPPER, url.url) is not None:

            # extract ID
            mapperID = url.url.split('/')[4]

            # set request
            requestUrl = BEATSAVER_API_MAP_BY_KEY + "/" + mapperID
            headers = {"User-Agent": USER_AGENT}
            req = request.Request(requestUrl, headers=headers)

            # send request
            try:
                response = request.urlopen(req)
                responseJson = json.load(response)
            except Exception:
                raise OriginalException(ErrorMessages.APIErrorMessage())

            # generate Song instances
            for songInfo in responseJson["docs"]:

                song = Song(
                    songID=SongID(songInfo["key"]),
                    hash=SongHash(songInfo["hash"])
                )
                songs.append(song)

        # beast saber (map)
        elif re.search(BEASTSABER_RE_URL_MAP, url.url) is not None:

            # extract key
            songKey = url.url.split('/')[4]

            # set request
            requestUrl = BEATSAVER_API_MAP_BY_KEY + "/" + songKey
            headers = {"User-Agent": USER_AGENT}
            req = request.Request(requestUrl, headers=headers)

            # send request
            try:
                response = request.urlopen(req)
                responseJson = json.load(response)
            except Exception:
                raise OriginalException(ErrorMessages.APIErrorMessage())

            # generate Song instance
            song = Song(
                songID=SongID(songKey),
                hash=SongHash(responseJson["hash"])
            )
            songs.append(song)

        # beast saber (mapper)
        elif re.search(BEASTSABER_RE_URL_MAPPER, url.url) is not None:

            # raise error (beast saberはmapperID管理が異なるため)
            raise OriginalException(
                ErrorMessages.GetURLForMapperErrorMessage())

        # return
        return songs

    # hash値からSongインスタンスを生成する
    def generateByHash(self, hash: SongHash) -> Song:

        # set request
        requestUrl = BEATSAVER_API_MAP_BY_HASH + "/" + hash.hash
        headers = {"User-Agent": USER_AGENT}
        req = request.Request(requestUrl, headers=headers)

        # send request
        try:
            response = request.urlopen(req)
            responseJson = json.load(response)
        except Exception:
            raise OriginalException(ErrorMessages.APIErrorMessage())

        # generate Song instance
        song = Song(
            songID=SongID(responseJson["key"]),
            hash=hash
        )

        # return
        return song
