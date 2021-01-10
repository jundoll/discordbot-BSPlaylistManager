
# load modules
import os
import traceback
import inject
from discord.ext import commands
from src.Factory.Abstract.ImageFactory import IImageFactory
from src.Factory.Abstract.SongFactory import ISongFactory
from src.Factory.Concrete.API.SongFactory import SongFactory
from src.Factory.Concrete.templateFile.ImageFactory import ImageFactory
from src.Repository.Abstract.PlaylistRepository import IPlaylistRepository
from src.Repository.Abstract.SongRepository import ISongRepository
from src.Repository.Concrete.Dropbox.PlaylistRepository import PlaylistRepository
from src.Repository.Concrete.Dropbox.SongRepository import SongRepository


# init settings
TOKEN = os.environ['DISCORD_BOT_TOKEN']
# 読み込むコグの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'src.Cog.PlaylistAdd',
    'src.Cog.PlaylistDelete',
    'src.Cog.PlaylistUpdate',
    'src.Cog.PlaylistOthers'
]


class StartUp:
    # DI Container部（リポジトリの実装クラスを指定する）

    # injection設定を指定する
    def def_inject_config(self, binder):
        binder.bind(IPlaylistRepository, PlaylistRepository())
        binder.bind(ISongFactory, SongFactory())
        binder.bind(IImageFactory, ImageFactory())
        binder.bind(ISongRepository, SongRepository())

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
    bot.run(TOKEN)
