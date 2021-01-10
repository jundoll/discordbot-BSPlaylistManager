
# load modules
import base64
import json
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
    def _generateEmbedLink(self, playlists: List[Playlist]) -> Tuple[List[File], List[Embed], List[str]]:

        # prepare return
        fileList = []
        embedList = []
        imageFilePathList = []

        for i, playlist in enumerate(playlists):
            # テキスト情報を追加する
            embed = discord.Embed(
                title="FileName", description="{}.json".format(playlist.fileName.filename), color=discord.Color.dark_orange())
            embed.add_field(
                name="Keyword", value=playlist.keyword.keyword, inline=False)
            embed.add_field(
                name="Title", value=playlist.title.title, inline=False)
            embed.add_field(
                name="Author", value=playlist.author.author, inline=False)
            embed.add_field(
                name="Description", value=playlist.description.description, inline=False)
            embed.add_field(name="Songs", value=len(
                playlist.songIDs), inline=False)

            # write image
            imageFileName = "thumbnail{}.png".format(i)
            imageFilePath = "Image/{}".format(imageFileName)
            imageFilePathList.append(imageFilePath)
            with open(imageFilePath, 'wb') as f:
                imageData = base64.b64decode(
                    playlist.image.image.split(";base64,")[1])
                f.write(imageData)

            file = discord.File(imageFilePath, filename=imageFileName)
            embed.set_thumbnail(url="attachment://{}".format(imageFileName))

            # append
            fileList.append(file)
            embedList.append(embed)

        # return
        return (fileList, embedList, imageFilePathList)

    # プレイリストの画像付き埋め込みリンクを作成する
    def _generateEmbedLinkByJson(self, playlistJson: Dict, playlist: Playlist) -> Tuple[List[File], Embed]:

        # テキスト情報を追加する
        embed = discord.Embed(
            title="Keyword", description=playlist.keyword.keyword, color=discord.Color.dark_blue())
        embed.add_field(
            name="Title", value=playlistJson["playlistTitle"], inline=False)
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

        # write json
        with open("downloadPlaylist.json", 'w') as f:
            json.dump(playlistJson, f)

        # ファイル情報を登録する
        files = []
        files.append(discord.File(
            "Image/thumbnail.png", filename="thumbnail.png"))
        files.append(discord.File(
            "downloadPlaylist.json", filename="{}.json".format(playlist.fileName.filename)))
        embed.set_thumbnail(url="attachment://thumbnail.png")

        # return
        return (files, embed)

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
            msg, playlistJson, playlist = self.playlistApplicationService.download(
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
        files, embed = self._generateEmbedLinkByJson(playlistJson, playlist)
        await ctx.send(msg, files=files, embed=embed)
        os.remove("downloadPlaylist.json")

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
        fileList, embedList, pathList = self._generateEmbedLink(playlists)
        msgFlag = True
        for file, embed, path in zip(fileList, embedList, pathList):
            # send message
            if msgFlag:
                await ctx.send(msg, file=file, embed=embed)
                msgFlag = False
            else:
                await ctx.send(file=file, embed=embed)
            # delete file
            os.remove(path)

    @ commands.command()
    async def usage(self, ctx):
        await ctx.send("使い方はこちらを見てね！\nhttps://github.com/jundoll/discordbot-BSPlaylistManager")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(PlaylistOthers(bot))
