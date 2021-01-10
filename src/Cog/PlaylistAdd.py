
# load modules
import os
import traceback
from discord.ext import commands
from src.ApplicationService.PlaylistApplicationService import PlaylistApplicationService
from src.Message.Error import OriginalException


# init settings
IS_DEV = os.environ['IS_DEV_BINARY'] == str(1)


# コグとして用いるクラスを定義。
class PlaylistAdd(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()

    @commands.group(invoke_without_command=True)
    async def add(self, ctx, arg_keyword, arg_url):
        '''お試し add'''

        # add song to playlist that has the keyword
        try:
            self.playlistApplicationService.addSong(arg_keyword, arg_url)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

    @add.command(aliases=['p', 'pl'])
    async def playlist(self, ctx, arg_title):
        '''お試し add pl'''

        # create new playlist
        try:
            self.playlistApplicationService.addPlaylist(arg_title)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

    @commands.command(aliases=['reg', 'regist'])
    async def register(self, ctx, arg_keyword, arg_url=""):

        # register playlist
        if len(arg_url) == 0:
            if ctx.message.attachments:
                attachment_url: str = ctx.message.attachments[0].url
            else:
                await ctx.send("アップロードするときのコメントにコマンドを入れてね！")
                return
        else:
            attachment_url = arg_url

        try:
            await ctx.send("ちょっと時間がかかるかもしれないよ！")
            await self.playlistApplicationService.registerPlaylist(arg_keyword, attachment_url)
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
    bot.add_cog(PlaylistAdd(bot))
