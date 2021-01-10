
# load modules
import os
import traceback
from discord.ext import commands
from src.ApplicationService.PlaylistApplicationService import PlaylistApplicationService
from src.Message.Error import OriginalException


# init settings
IS_DEV = os.environ['IS_DEV_BINARY'] == str(1)


# コグとして用いるクラスを定義。
class PlaylistUpdate(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()

    @commands.group(invoke_without_command=True, aliases=['ch'])
    async def update(self, ctx):
        pass

    @update.command()
    async def filename(self, ctx, arg_trg_keyword, arg_filename):

        # update filename
        try:
            self.playlistApplicationService.updateFileName(
                arg_trg_keyword, arg_filename)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

    @update.command()
    async def keyword(self, ctx, arg_trg_keyword, arg_new_keyword):

        # update keyword
        try:
            self.playlistApplicationService.updateKeyword(
                arg_trg_keyword, arg_new_keyword)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

    @update.command()
    async def title(self, ctx, arg_trg_keyword, arg_title):

        # update title
        try:
            self.playlistApplicationService.updateTitle(
                arg_trg_keyword, arg_title)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

    @update.command()
    async def author(self, ctx, arg_trg_keyword, arg_author):

        # update author
        try:
            self.playlistApplicationService.updateAuthor(
                arg_trg_keyword, arg_author)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

    @update.command()
    async def desc(self, ctx, arg_trg_keyword, arg_desc):

        # update description
        try:
            self.playlistApplicationService.updateDescription(
                arg_trg_keyword, arg_desc)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

    @update.command()
    async def img(self, ctx, arg_trg_keyword, arg_url=""):

        # register playlist
        if len(arg_url) == 0:
            attachment_url: str = ctx.message.attachments[0].url
            if attachment_url is None:
                await ctx.send("アップロードするときのコメントにコマンドを入れてね！")
                return
        else:
            attachment_url = arg_url

        # update image
        try:
            self.playlistApplicationService.updateImage(
                arg_trg_keyword, attachment_url)
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
    bot.add_cog(PlaylistUpdate(bot))
