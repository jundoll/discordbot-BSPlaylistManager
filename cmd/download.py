
# load modules
import os


# init settings
dl_path = os.environ['BS_PLAYLIST_DL_PATH']


# definition
async def reply(ctx):

    # set reply message
    reply = "お試しよ！　" + dl_path

    # send
    await ctx.send(reply)
