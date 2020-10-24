
# load modules
import dropbox
from urllib import request
from lxml import html
from discord.ext import commands
import os
import traceback
import hashlib
import json


# init settings
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
is_dev = os.environ['IS_DEV_BINARY'] == str(1)
dropbox_token = os.environ['DROPBOX_ACCESS_TOKEN']
dropbox_path = 'BSPlaylistManager-dev' if is_dev else 'BSPlaylistManager'


# define class
class MyDropbox():

    def __init__(self):
        self.dbx = dropbox.Dropbox(dropbox_token)
        res = self.dbx.files_list_folder("", recursive=True)
        for entry in res.entries:
            if entry.path_display.startswith("/"+dropbox_path+"/"):
                self.fpath = entry.path_lower

    def get_shared_link(self):
        links = self.dbx.sharing_list_shared_links(
            path=self.fpath, direct_only=True).links

        if links is not None:
            for link in links:
                return link.url.replace("dl=0", "dl=1")

        return self.__create_shared_link()

    def __create_shared_link(self):
        setting = dropbox.sharing.SharedLinkSettings(
            requested_visibility=dropbox.sharing.RequestedVisibility.public)
        link = self.dbx.sharing_create_shared_link_with_settings(
            path=self.fpath, settings=setting)

        return link.url.replace("dl=0", "dl=1")

    def update_playlist(self, url: str, songInfo: dict):

        # load playlist
        playlist = request.urlopen(url).read()
        playlist = json.loads(playlist)

        # add song
        playlist['songs'] += [songInfo]
        playlist['songs'] = [dict(t) for t in {tuple(
            d.items()) for d in playlist['songs']}]

        # update playlist
        bytes_playlist = bytes(json.dumps(playlist, separators=(
            ',', ':'), ensure_ascii=False), encoding="utf-8")
        self.dbx.files_upload(bytes_playlist, self.fpath,
                              mode=dropbox.files.WriteMode.overwrite)


# define function
def getSongInfo(url: str):

    # もし他に引数があったらエラーキャッチしないと。

    # 今のところはbsaber.comだけを受け付ける。
    # 受け付けないものはエラーを返す（後でキャッチ）
    try:
        flag = False
        for url_split in url.split('/'):
            if url_split == 'bsaber.com':
                flag = True
        if not flag:
            raise Exception
    except Exception:
        raise Exception

    # スクレイピング
    data = request.urlopen(url)
    raw_html = data.read()
    format_html = html.fromstring(str(raw_html))

    # 曲名
    song_name = format_html.xpath(
        '//*[@id="infinite-article"]/div[1]/div[1]/div[2]/div/div/header/h1')[0].text

    # hash値
    dl_url = format_html.xpath(
        '//*[@id="infinite-article"]/div[1]/div[1]/div[2]/div/div/header/div[4]/a[3]/@href')[0]
    hash = dl_url.split('/')[-1].split('.')[0]

    # return
    song_dict = dict.fromkeys(['songName', 'hash'])
    song_dict['songName'] = song_name
    song_dict['hash'] = hash
    return song_dict


def get_song_info(songFolderPath: str):

    # init
    song_dict = dict.fromkeys(['songName', 'hash'])

    # load data
    # songFolderPath = "C:/Program Files (x86)/Steam/steamapps/common/Beat Saber/Beat Saber_Data/CustomLevels/78cb (Burning Chaos According to the Sun - kolezan)"
    with open(songFolderPath+"/info.dat") as f:
        infoDat_json = json.load(f)

    # get songName
    if "_songName" in infoDat_json.keys():
        song_dict['songName'] = infoDat_json['_songName']

    # generate hash
    combinedBytes = bytes()
    with open(songFolderPath+"/info.dat") as f:
        combinedBytes = f.read().encode()

    if "_difficultyBeatmapSets" in infoDat_json.keys():
        for mapSets in infoDat_json['_difficultyBeatmapSets']:
            if "_difficultyBeatmaps" in mapSets.keys():
                for maps in mapSets["_difficultyBeatmaps"]:
                    if "_beatmapFilename" in maps.keys():
                        with open(songFolderPath+"/"+maps["_beatmapFilename"]) as f:
                            combinedBytes = combinedBytes + f.read().encode()

    hash = hashlib.sha1(combinedBytes).hexdigest()
    song_dict['hash'] = hash

    # return
    return hash


# set command
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(
        traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def add(ctx, arg):
    playlist_url = myDropbox.get_shared_link()
    songInfo = getSongInfo(arg)
    myDropbox.update_playlist(playlist_url, songInfo)
    await ctx.send("Successfully Adding Song!")


@bot.command()
async def download(ctx):
    playlist_url = myDropbox.get_shared_link()
    await ctx.send("これをお使い！ "+playlist_url)


# do
myDropbox = MyDropbox()


# run
bot.run(token)
