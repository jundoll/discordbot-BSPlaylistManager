
# load modules
from Application.PlaylistApplicationService import PlaylistApplicationService
from Application.SongApplicationService import SongApplicationService
from discord.ext import commands


# コグとして用いるクラスを定義。
class PlaylistUpdateInfo(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()
        self.songApplicationService = SongApplicationService()

    @commands.group(invoke_without_command=True, aliases=['ch'])
    async def update(self, ctx):
        pass

    @update.command()
    async def filename(self, ctx, arg_trg_title, arg_filename):
        # get playlist path
        self.playlistApplicationService.updateFileName(arg_trg_title, arg_filename)
        # return console
        await ctx.send("タイトル「" + arg_trg_title + "」のファイル名を「" + arg_filename + "」に変更したよ！")

    @update.command()
    async def title(self, ctx, arg_trg_title, arg_new_title):
        # get playlist path
        self.playlistApplicationService.updateTitle(arg_trg_title, arg_new_title)
        # return console
        await ctx.send("タイトル「" + arg_trg_title + "」を「" + arg_new_title + "」に変更したよ！")

    @update.command()
    async def author(self, ctx, arg_trg_title, arg_author):
        # get playlist path
        self.playlistApplicationService.updateAuthor(arg_trg_title, arg_author)
        # return console
        await ctx.send("タイトル「" + arg_trg_title + "」の作成者を「" + arg_author + "」に変更したよ！")

    @update.command()
    async def desc(self, ctx, arg_trg_title, arg_desc):
        # get playlist path
        self.playlistApplicationService.updateDescription(arg_trg_title, arg_desc)
        # return console
        await ctx.send("タイトル「" + arg_trg_title + "」の説明を「" + arg_desc + "」に変更したよ！")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(PlaylistUpdateInfo(bot))

