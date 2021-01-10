
# load modules
import os
import traceback
from discord.ext import commands
from src.ApplicationService.PlaylistApplicationService import PlaylistApplicationService
from src.Message.Error import OriginalException


# init settings
IS_DEV = os.environ['IS_DEV_BINARY'] == str(1)


# コグとして用いるクラスを定義。
class PlaylistDelete(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()

    @commands.group(invoke_without_command=True, aliases=['del'])
    async def delete(self, ctx, arg_title, arg_url):

        # del song to playlist that has the keyword
        try:
            self.playlistApplicationService.deleteSong(arg_title, arg_url)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

    @delete.command()
    async def pl(self, ctx, arg_title):

        # delete the playlist
        try:
            self.playlistApplicationService.deletePlaylist(arg_title)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

    @commands.command()
    async def restore(self, ctx, arg_keyword):

        # restore the playlist
        try:
            self.playlistApplicationService.restorePlaylist(arg_keyword)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(PlaylistDelete(bot))
