
# load modules
import dropbox
from discord.ext import commands
import os
import traceback


# init settings
bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']
is_dev = os.environ['IS_DEV_BINARY'] == str(1)
dropbox_token = os.environ['DROPBOX_ACCESS_TOKEN']
dropbox_path = 'BSPlaylistManager-dev' if is_dev else 'BSPlaylistManager'


# set command
@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(
        traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def download(ctx):
    playlist_url = "myDropbox.get_shared_link()"
    await ctx.send("これをお使い！ "+playlist_url)


# run
bot.run(token)
