
# load modules
from Application.SongApplicationService import SongApplicationService
from Application.PlaylistApplicationService import PlaylistApplicationService
from discord.ext import commands


# コグとして用いるクラスを定義。
class PlaylistManager(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()
        self.songApplicationService = SongApplicationService()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        orig_error = getattr(error, "original", error)
        await ctx.send(orig_error.args[0])

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

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


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(PlaylistManager(bot))
