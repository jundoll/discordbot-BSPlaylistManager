
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

    def add_song(self, url: str, songInfo: dict):

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

    def del_song(self, url: str, songInfo: dict):

        # load playlist
        playlist = request.urlopen(url).read()
        playlist = json.loads(playlist)

        # del song
        try:
            playlist['songs'].remove(songInfo)
        except Exception:
            pass

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

    # hash値
    dl_url = format_html.xpath(
        '//*[@id="infinite-article"]/div[1]/div[1]/div[2]/div/div/header/div[4]/a[3]/@href')[0]
    hash = dl_url.split('/')[-1].split('.')[0]

    # return
    song_dict = dict.fromkeys(['hash'])
    song_dict['hash'] = hash
    return song_dict


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
    myDropbox.add_song(playlist_url, songInfo)
    await ctx.send("リストに追加したよ！")


@bot.command()
async def delete(ctx, arg):
    playlist_url = myDropbox.get_shared_link()
    songInfo = getSongInfo(arg)
    myDropbox.del_song(playlist_url, songInfo)
    await ctx.send("リストから削除したよ！")


@bot.command()
async def download(ctx):
    playlist_url = myDropbox.get_shared_link()
    await ctx.send("これをお使い！ "+playlist_url)


@bot.command()
async def dl(ctx):
    playlist_url = myDropbox.get_shared_link()
    await ctx.send("これをお使い！ "+playlist_url)


# do
myDropbox = MyDropbox()


# run
bot.run(token)
