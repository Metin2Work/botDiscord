from discord.ext import commands
import asyncio
import discord

time_temp_messages = 5


class ModCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

    @commands.command(name="clear", pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount="all"):
        if amount == "all":
            deleted = await ctx.message.channel.purge(limit=9999999)
            message = await ctx.send('Deleted {} message(s)'.format(len(deleted) - 1))
        else:
            deleted = await ctx.message.channel.purge(limit=int(amount) + 1)
            message = await ctx.send('Deleted {} message(s)'.format(len(deleted) - 1))

        await asyncio.sleep(time_temp_messages)

        await message.delete()

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, *reason):
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await member.ban(reason=reason)
            await ctx.send("Member banned.")
        else:
            await ctx.send('Member not found.')

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send("Member unbanned.")

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *reason):
        if member is not None:
            if reason:
                reason = ' '.join(reason)
            else:
                reason = None
            await member.kick(reason=reason)
            await ctx.send("And he leaves us...")
        else:
            await ctx.send('Member not found.')

    @commands.command(name="poll", aliases=["sondage", "vote"])
    async def poll(self, ctx, question="", *answers):
        if question == "":
            await ctx.send('Notice: =poll "question" "answer" "answer"')
            return
        if len(answers) == 1:
            await ctx.send("You must specify two answers.")
            return
        if len(answers) > 5:
            await ctx.send("You can not specify more than five answers.")
            return

        if len(answers) == 2 and (answers[0] == "yes" or answers[0] == "oui") and (
                answers[1] == "no" or answers[1] == "non"):
            reactions = ['🇦', '🇧']
            answers = ("Yes", "No")
        elif len(answers) == 0:
            reactions = ['🇦', '🇧']
            answers = ("Yes", "No")
        else:
            reactions = ['🇦', '🇧', '🇨', '🇩', '🇪']

        description = []

        for x, answer in enumerate(answers):
            description += '\n {} {}'.format(reactions[x], answer)

        await ctx.send("📊 **" + question + "** @everyone")
        embed = discord.Embed(title="", description=''.join(description), color=discord.Color(0xCE181E))
        react_message = await ctx.send(embed=embed)

        for reaction in reactions[:len(answers)]:
            await react_message.add_reaction(reaction)


def setup(client):
    client.add_cog(ModCog(client))
