
# load modules
from Application.PlaylistApplicationService import PlaylistApplicationService
from Application.SongApplicationService import SongApplicationService
from discord.ext import commands


# コグとして用いるクラスを定義。
class PlaylistDelete(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()
        self.songApplicationService = SongApplicationService()

    @commands.group(invoke_without_command=True, aliases=['del'])
    async def delete(self, ctx, arg_title, arg_url):
        # del song to the playlist
        self.songApplicationService.delete(arg_title, arg_url)
        # return console
        await ctx.send("タイトル「" + arg_title + "」のプレイリストから削除したよ！")

    @delete.command()
    async def pl(self, ctx, arg_title):
        # get playlist path
        self.playlistApplicationService.delete(arg_title)
        # return console
        await ctx.send("タイトル「" + arg_title + "」のプレイリストを削除したよ！")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(PlaylistDelete(bot))
