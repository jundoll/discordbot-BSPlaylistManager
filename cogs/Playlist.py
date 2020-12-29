from discord.ext import commands


# コグとして用いるクラスを定義。
class PlaylistManager(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

    @commands.command()
    async def add_empty_playlist(self):
        print(1)

    @commands.command()
    async def delete_empty_playlist(self):
        print(1)

    @commands.command()
    async def delete_playlist(self):
        print(1)

    @commands.command()
    async def get_shared_link(self):
        links = self.dbx.sharing_list_shared_links(
            path=self.fpath, direct_only=True).links

        if links is not None:
            for link in links:
                return link.url.replace("dl=0", "dl=1")

        return self.__create_shared_link()


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(PlaylistManager(bot))  # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
