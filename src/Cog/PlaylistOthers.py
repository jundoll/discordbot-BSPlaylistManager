
# load modules
import base64
import os
import traceback
from typing import Dict, List, Tuple
import discord
from discord.embeds import Embed
from discord.ext import commands
from discord.file import File
from src.ApplicationService.PlaylistApplicationService import PlaylistApplicationService
from src.Domain.Playlist import Playlist
from src.Message.Error import OriginalException


# init settings
IS_DEV = os.environ['IS_DEV_BINARY'] == str(1)


# コグとして用いるクラスを定義。
class PlaylistOthers(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()

    # 複数のプレイリストに対して埋め込みリンクを作成する
    def _generateSimpleEmbedLink(self, playlists: List[Playlist]) -> List[Embed]:

        # prepare return
        embedList = []

        for playlist in playlists:
            # テキスト情報を追加する
            embed = discord.Embed(
                title="FileName", description=playlist.fileName.filename, color=discord.Color.dark_orange())
            embed.add_field(name="Keyword", value=playlist.author.author)
            embed.add_field(name="Title", value=playlist.title.title)
            embed.add_field(name="Author", value=playlist.author.author)
            embed.add_field(name="Songs", value=len(
                playlist.songIDs), inline=False)

            # append
            embedList.append(embed)

        # return
        return embedList

    # プレイリストの画像付き埋め込みリンクを作成する
    def _generateFullEmbedLinkByJson(self, playlistJson: Dict) -> Tuple[File, Embed]:

        # テキスト情報を追加する
        embed = discord.Embed(
            title="Title", description=playlistJson["playlistTitle"], color=discord.Color.dark_blue())
        embed.add_field(
            name="Author", value=playlistJson["playlistAuthor"], inline=False)
        embed.add_field(
            name="Description", value=playlistJson["playlistDescription"]+'\u200b', inline=False)
        embed.add_field(name="Songs", value=len(
            playlistJson["songs"]), inline=False)

        # write image
        with open("Image/thumbnail.png", 'wb') as f:
            imageData = base64.b64decode(
                playlistJson["image"].split(";base64,")[1])
            f.write(imageData)

        # 画像情報を追加する
        file = discord.File("Image/thumbnail.png", filename="thumbnail.png")
        embed.set_thumbnail(url="attachment://thumbnail.png")

        # return
        return (file, embed)

    # error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandNotFound):
            await ctx.send('そんなコマンド無いよ！使い方を確認してね！')

        elif isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send('入力が間違ってるよ！使い方を確認してね！')

        elif isinstance(error, OriginalException):
            org_msg = getattr(error, "original", error)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])

        else:
            orig_error = getattr(error, "original", error)
            await ctx.send('想定外のエラーだよ！管理者に伝えてあげてね！\n' + ''.join(
                traceback.TracebackException.from_exception(orig_error).format()))

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(aliases=['dl'])
    async def download(self, ctx, arg_trg_keyword):

        try:
            # get playlist url
            msg, playlistJson = self.playlistApplicationService.download(
                arg_trg_keyword)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])
            return

        # make embed
        file, embed = self._generateFullEmbedLinkByJson(playlistJson)
        await ctx.send(msg, file=file, embed=embed)

    @ commands.command(aliases=['s'])
    async def search(self, ctx, arg_search_keyword):

        try:
            msg, playlists = self.playlistApplicationService.search(
                arg_search_keyword)
        except OriginalException as e:
            # return message
            org_msg = getattr(e, "original", e)
            if IS_DEV:
                await ctx.send(''.join(traceback.TracebackException.from_exception(org_msg).format()))
            else:
                await ctx.send(org_msg.args[0])
            return

        # make embed
        embedList = self._generateSimpleEmbedLink(playlists)
        for embed in embedList:
            await ctx.send(msg, embed=embed)

    @ commands.command()
    async def usage(self, ctx):
        await ctx.send("使い方はこちらを見てね！\nhttps://github.com/jundoll/discordbot-BSPlaylistManager")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(PlaylistOthers(bot))
