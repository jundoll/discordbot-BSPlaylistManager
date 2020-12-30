
# load modules
import os
import traceback
from Application.PlaylistApplicationService import PlaylistApplicationService
from discord.ext import commands


# init settings
is_dev = os.environ['IS_DEV_BINARY'] == str(1)


# コグとして用いるクラスを定義。
class PlaylistOthers(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()

    # error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('そんなコマンド無いよ！使い方を確認してね！')
        elif isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send('入力が間違ってるよ！使い方を確認してね！')
        elif isinstance(error, (FileNotFoundError)):
            orig_error = getattr(error, "original", error)
            await ctx.send('想定外のエラーだよ！管理者に伝えてあげてね！\n' + ''.join(
                traceback.TracebackException.from_exception(orig_error).format()))
        else:
            orig_error = getattr(error, "original", error)
            if is_dev:
                await ctx.send(''.join(traceback.TracebackException.from_exception(orig_error).format()))
            else:
                await ctx.send(orig_error.args[0])

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(aliases=['dl'])
    async def download(self, ctx, arg_title):
        # get playlist url
        playlistUrl = self.playlistApplicationService.getDownloadUrl(arg_title)
        # return console
        await ctx.send("これをお使い！ " + playlistUrl)

    @commands.command()
    async def help(self, ctx):
        # return console
        await ctx.send("使い方はこちらを見てね！\nhttps://github.com/jundoll/discordbot-BSPlaylistManager")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(PlaylistOthers(bot))