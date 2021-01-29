import discord
import os
from discord.ext import commands
from inc import STATICS
from discord.ext.commands import CommandNotFound

__author__ = "Takuma"
__version__ = "1.0"

client = commands.Bot(command_prefix=STATICS.PREFIX, case_insensitive=STATICS.CASE_INSENSITIVE)

if __name__ == "__main__":
    for extension in os.listdir("inc/cogs/"):
        if extension.endswith(".py"):
            extension = "inc.cogs." + extension[:-3]
            try:
                client.load_extension(extension)
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {} \n {}'.format(extension, exc))


@client.event
async def on_ready():
    print('Logged in as {0} with user_id : {1}'.format(client.user.name, client.user.id))
    print('------')

    await client.change_presence(status=STATICS.STATUS, activity=discord.Game(STATICS.GAME))


@client.event
async def on_command_error(ctx, error):
    """
    When unknown command
    :param ctx: Context
    :param error: Error
    :return: None
    """
    if isinstance(error, CommandNotFound):
        return
    raise error

# Launch bot
client.run(STATICS.TOKEN)