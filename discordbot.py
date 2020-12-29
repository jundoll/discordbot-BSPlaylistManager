
# load modules
import os
import traceback
import inject
from Application.SongApplicationService import SongApplicationService
from Application.PlaylistApplicationService import PlaylistApplicationService
from discord.ext import commands
from Factory.SongFactory import ISongFactory, SongFactory
from Repository.Dropbox.PlaylistRepositoryDropbox import PlaylistRepositoryDropbox
from Repository.PlaylistRepository import IPlaylistRepository

# init settings
token = os.environ['DISCORD_BOT_TOKEN']
# 読み込むコグの名前を格納しておく。
INITIAL_EXTENSIONS = ['cogs.PlaylistManager']


class StartUp:
    # DI Container部（リポジトリの実装クラスを指定する）

    # injection設定を指定する
    def def_inject_config(self, binder):
        binder.bind(IPlaylistRepository, PlaylistRepositoryDropbox())
        binder.bind(ISongFactory, SongFactory())

    # injection設定を適用する関数
    def set_config(self):
        inject.configure(self.def_inject_config)


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

        self.playlistApplicationService = PlaylistApplicationService()
        self.songApplicationService = SongApplicationService()

    # set event
    # @commands.event
    # async def on_command_error(self, ctx, error):
    #    orig_error = getattr(error, "original", error)
    #    error_msg = ''.join(
    #        traceback.TracebackException.from_exception(orig_error).format())
    #    await ctx.send(error_msg)

    # set command

    @commands.group(invoke_without_command=True)
    async def add(self, ctx, arg_title, arg_url):
        # add song to the playlist
        self.songApplicationService.add(arg_title, arg_url)
        # return console
        await ctx.send("タイトル「" + arg_title + "」のプレイリストに追加したよ！")
        # messageはエラーが出なかった場合のみにしたい。重複のときはエラーにしたい。
        # 重複--> mapper指定での追加のときはかぶりが多く発生するので悩みどころ。

    @add.command(alises=['pl', 'playlist'])
    async def pl_add(self, ctx, arg_title):
        # get playlist path
        self.playlistApplicationService.create(arg_title)
        # return console
        await ctx.send("プレイリストを作成したよ！タイトル「" + arg_title + "」を使って曲を追加してね！")

    @commands.group(invoke_without_command=True, aliases=['del'])
    async def delete(self, ctx, arg_title, arg_url):
        # del song to the playlist
        self.songApplicationService.delete(arg_title, arg_url)
        # return console
        await ctx.send("タイトル「" + arg_title + "」のプレイリストから削除したよ！")

    @delete.command(alises=['pl', 'playlist'])
    async def pl_del(self, ctx, arg_title):
        # get playlist path
        self.playlistApplicationService.delete(arg_title)
        # return console
        await ctx.send("タイトル「" + arg_title + "」のプレイリストを削除したよ！")

    @commands.command(aliases=['dl'])
    async def download(self, ctx, arg_title):
        # get playlist url
        playlistUrl = self.playlistApplicationService.getDownloadUrl(arg_title)
        # return console
        await ctx.send("これをお使い！ " + playlistUrl)


# botのインスタンス化及び起動処理
if __name__ == '__main__':

    # inject startup
    startUp = StartUp()
    startUp.set_config()

    # launch bot
    bot = DiscordBot(command_prefix='/')
    bot.run(token)
