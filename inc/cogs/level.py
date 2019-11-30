import json
import time
import os

import discord
from discord.ext import commands

# Constant
min_time_between_msg = 30
exp_per_msg = 5
level_difficulty = 4

# int(level) : [rank, rank] --> positive to add the rank, and negative to remove.
rank_role = {
    # 5: []
}


async def update_data(file_data, member):
    """
    Check if experience profile's player exist
    :param file_data: json data
    :param member: member object
    """
    if not str(member.id) in file_data:
        file_data[str(member.id)] = {}
        file_data[str(member.id)]["experience"] = 0
        file_data[str(member.id)]["level"] = 1
        file_data[str(member.id)]["last_message"] = int(time.time())


async def add_experience(file_data, member, exp):
    """
    Add experience
    :param file_data:  JSON with players' data
    :param member: Member object
    :param exp: count of exp
    """
    if file_data[str(member.id)]["last_message"] < int(time.time()) - min_time_between_msg:
        file_data[str(member.id)]["experience"] += exp
        file_data[str(member.id)]["last_message"] = int(time.time())


async def level_up(file_data, member, channel):
    """
    Increase the level if it possible.
    :param file_data: JSON with players' data
    :param member: Member object
    :param channel: Channel object
    """
    experience = file_data[str(member.id)]["experience"]
    lvl_start = file_data[str(member.id)]["level"]
    lvl_end = int(experience ** (1 / level_difficulty))

    if lvl_start < lvl_end:
        await channel.send("{} has leveled up to level {} !".format(member.mention, lvl_end))
        file_data[str(member.id)]['level'] = lvl_end

        if lvl_end in rank_role:
            add_rank = []
            del_rank = []
            for i in rank_role[lvl_end]:
                if i > 0:
                    add_rank.append(i)
                else:
                    del_rank.append(i * (-1))
            # Add rank
            for i, val in enumerate(add_rank):
                await member.add_roles(discord.utils.get(member.guild.roles, id=val))

            # Del rank
            for i, val in enumerate(del_rank):
                await member.remove_roles(discord.utils.get(member.guild.roles, id=val))


class LevelCog(commands.Cog):
    def __init__(self, client):
        self.bot = client

        # Check if configuration exist :
        if not os.path.isdir("inc/data/level"):
            os.makedirs("inc/data/level/")
        if not os.path.exists("inc/data/level/level.json"):
            print("Level: No configuration found.")
            print("Level: Initialize default configuration..")
            with open("inc/data/level/level.json", "w") as f:
                f.write("{}")

    @commands.command(name="rank", pass_context=True)
    async def rank(self, ctx):
        """
        Get your rank
        :param ctx: context
        """
        with open("inc/data/level/level.json", "r") as file:
            fileData = json.load(file)

        i = 0
        count = 0
        while i < (fileData[str(ctx.author.id)]["level"] + 1):
            i = int((fileData[str(ctx.author.id)]["experience"] + (count * exp_per_msg)) ** (1 / level_difficulty))
            count += 1

        await ctx.send("{}".format(ctx.author.mention))

        embed = discord.Embed(title='', colour=0xCE181E)
        embed.add_field(name='Lvl.', value=fileData[str(ctx.author.id)]["level"], inline=True)
        embed.add_field(name='Exp.',
                        value='total : {}'.format(fileData[str(ctx.author.id)]["experience"]), inline=True)
        embed.add_field(name='Next level :', value=str(count) + " messages", inline=True)
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        embed.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="top", pass_context=True)
    async def top(self, ctx):
        """
        get top level
        :param ctx: context
        """
        with open("inc/data/level/level.json", "r") as file:
            fileData = json.load(file)

        top = sorted(fileData, key=lambda x: int(x), reverse=True)[:5]
        message = []

        count = 0
        top_emoji = [":one:", ":two:", "!trhee:", ":four:", ":five:"]

        for item in top:
            message.append("{} {}: {} exp !\n".format(top_emoji[count], self.bot.get_user(int(item)),
                                                      fileData[str(item)]["experience"]))
            count += 1

        embed = discord.Embed(title="Top : ", description=''.join(message), color=discord.Color(0xCE181E))
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Event : when member join discord
        :param member:
        """
        with open("inc/data/level/level.json", "r") as file:
            file_data = json.load(file)

        await update_data(file_data, member)

        with open("inc/data/level/level.json", "w") as file:
            json.dump(file_data, file)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Event : when member send a message
        :param message:
        """
        if message.author.id != self.bot.user.id:
            with open("inc/data/level/level.json", "r") as file:
                file_data = json.load(file)

            await update_data(file_data, message.author)
            await add_experience(file_data, message.author, exp_per_msg)
            await level_up(file_data, message.author, message.channel)

            with open("inc/data/level/level.json", "w") as file:
                json.dump(file_data, file)


def setup(client):
    client.add_cog(LevelCog(client))
