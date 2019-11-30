import discord
from discord.ext import commands


class AdminCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(name="shutdown", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        """
        Shutdown bot.
        :param ctx: context
        """
        await ctx.send("Bye my friend...")
        await ctx.bot.logout()

    @commands.command(name='reload')
    @commands.has_permissions(administrator=True)
    async def _reload(self, ctx, module: str):
        """
        Reload a module
        :param ctx: context
        :param module: module name
        """
        module = "inc.cogs." + module
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            print('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name="changeStatus")
    @commands.has_permissions(administrator=True)
    async def changestatus(self, ctx, status: str):
        """
        Change the bot's status
        :param ctx: context
        :param status: online/dnd/absent/off
        """
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle' or status == "absent":
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb' or status == "busy":
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        await self.bot.change_presence(status=discordStatus)

    @commands.command(name="changeAvatar")
    @commands.has_permissions(administrator=True)
    async def changeAvatar(self, ctx):
        """
        Update avatar image.
        :param ctx: context
        """
        # Avatar
        with open('inc/img/profile.jpg', 'rb') as f:
            await self.bot.user.edit(avatar=f.read())

    @commands.command(name="changeName")
    @commands.has_permissions(administrator=True)
    async def changeName(self, ctx, name: str):
        """
        Change bot's name
        :param ctx: context
        :param name: new name
        """
        await self.bot.user.edit(username=name)
        await ctx.send("My new name is {}".format(name))


def setup(client):
    client.add_cog(AdminCog(client))
