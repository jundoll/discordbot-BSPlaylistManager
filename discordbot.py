
# load modules
import dropbox
from urllib import request
from lxml import html
from discord.ext import commands
import os
import traceback
import json


# init settings
token = os.environ['DISCORD_BOT_TOKEN']
is_dev = os.environ['IS_DEV_BINARY'] == str(1)
dropbox_token = os.environ['DROPBOX_ACCESS_TOKEN']
dropbox_path = 'BSPlaylistManager-dev' if is_dev else 'BSPlaylistManager'
# 読み込むコグの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cogs.Playlist'
]


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


class DiscordBot(commands.Bot):

    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # define function
    def getSongInfo(self, url: str):

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

    # do
    myDropbox = MyDropbox()

    # set command
    @commands.event
    async def on_command_error(self, ctx, error):
        orig_error = getattr(error, "original", error)
        error_msg = ''.join(
            traceback.TracebackException.from_exception(orig_error).format())
        await ctx.send(error_msg)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command()
    async def add(self, ctx, arg):
        playlist_url = self.myDropbox.get_shared_link()
        songInfo = self.getSongInfo(arg)
        self.myDropbox.add_song(playlist_url, songInfo)
        await ctx.send("リストに追加したよ！")

    @commands.command(aliases=['del'])
    async def delete(self, ctx, arg):
        playlist_url = self.myDropbox.get_shared_link()
        songInfo = self.getSongInfo(arg)
        self.myDropbox.del_song(playlist_url, songInfo)
        await ctx.send("リストから削除したよ！")

    @commands.command(aliases=['dl'])
    async def download(self, ctx):
        playlist_url = self.myDropbox.get_shared_link()
        await ctx.send("これをお使い！ "+playlist_url)

    # Botの準備完了時に呼び出されるイベント
    # async def on_ready(self):
    #    print('-----')
    #    print(self.user.name)
    #    print(self.user.id)
    #    print('-----')


# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    bot = DiscordBot(command_prefix='/')
    bot.run(token)
