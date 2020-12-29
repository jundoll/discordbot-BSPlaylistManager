
# load modules
import os
import traceback
import inject
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


# botのインスタンス化及び起動処理
if __name__ == '__main__':

    # inject startup
    startUp = StartUp()
    startUp.set_config()

    # launch bot
    bot = DiscordBot(command_prefix='/')
    bot.run(token)
