
# load modules
from Domain.Playlist import ImageBase64
import base64
import io
import os
import traceback
import discord
from Application.PlaylistApplicationService import PlaylistApplicationService
from discord.ext import commands
import tempfile


# init settings
is_dev = os.environ['IS_DEV_BINARY'] == str(1)


# コグとして用いるクラスを定義。
class PlaylistOthers(commands.Cog):

    # Playlistクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

        self.playlistApplicationService = PlaylistApplicationService()

    # Base64の画像データを一時ファイルに保存し、そのパスを返す
    def genImageForEmbedLink(self, imageBase64: ImageBase64) -> str:

        # Base64の画像データを一時ファイルに保存し、そのパスを返す
        with tempfile.NamedTemporaryFile(delete=False) as tf:

            # write image
            with open(tf.name, 'wb') as f:
                imageData = base64.b64decode(
                    imageBase64.image.split(";base64,")[1])
                f.write(imageData)

            # return file path
            return tf.name

    # error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('そんなコマンド無いよ！使い方を確認してね！')
        elif isinstance(error, (commands.MissingRequiredArgument, commands.BadArgument)):
            await ctx.send('入力が間違ってるよ！使い方を確認してね！')
        elif isinstance(error, (FileNotFoundError)):
            orig_error = getattr(error, "original", error)
            await ctx.send('想定外のエラーだよ！管理者に伝えてあげてね！\n' + ''.join(
                traceback.TracebackException.from_exception(orig_error).format()))
        else:
            orig_error = getattr(error, "original", error)
            if is_dev:
                await ctx.send(''.join(traceback.TracebackException.from_exception(orig_error).format()))
            else:
                await ctx.send(orig_error.args[0])

    # コマンドの作成。コマンドはcommandデコレータで必ず修飾する。
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(aliases=['dl'])
    async def download(self, ctx, arg_title):
        # get playlist url
        playlistUrl = self.playlistApplicationService.getDownloadUrl(arg_title)
        # get playlist
        playlist = self.playlistApplicationService.find(arg_title)
        # make embed
        embed = discord.Embed(
            title="Title", description=arg_title, color=discord.Color.dark_blue())
        embed.add_field(
            name="Author", value=playlist.playlistAuthor.playlistAuthor, inline=False)
        embed.add_field(
            name="Description", value=playlist.playlistDescription.playlistDescription, inline=False)
        embed.add_field(name="Songs", value=len(playlist.songs), inline=False)
        embed.set_thumbnail(url=self.genImageForEmbedLink(playlist.image))
        # return console
        await ctx.send("これをお使い！ " + playlistUrl, embed=embed)

    @commands.command()
    async def usage(self, ctx):
        # return console
        await ctx.send("使い方はこちらを見てね！\nhttps://github.com/jundoll/discordbot-BSPlaylistManager")


# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    # PlaylistにBotを渡してインスタンス化し、Botにコグとして登録する。
    bot.add_cog(PlaylistOthers(bot))
