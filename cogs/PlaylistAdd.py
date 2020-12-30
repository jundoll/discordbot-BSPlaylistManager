
# load modules
from Application.PlaylistApplicationService import PlaylistApplicationService
from Application.SongApplicationService import SongApplicationService
from discord.ext import commands


# コグとして用いるクラスを定義。
class PlaylistAdd(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()
        self.songApplicationService = SongApplicationService()

    @commands.group(invoke_without_command=True)
    async def add(self, ctx, arg_title, arg_url):
        # add song to the playlist
        self.songApplicationService.add(arg_title, arg_url)
        # return console
        await ctx.send("タイトル「" + arg_title + "」のプレイリストに追加したよ！")
        # messageはエラーが出なかった場合のみにしたい。重複のときはエラーにしたい。
        # 重複--> mapper指定での追加のときはかぶりが多く発生するので悩みどころ。

    @add.command()
    async def pl(self, ctx, arg_title):
        # get playlist path
        self.playlistApplicationService.create(arg_title)
        # return console
        await ctx.send("プレイリストを作成したよ！タイトル「" + arg_title + "」を使って曲を追加してね！")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(PlaylistAdd(bot))
