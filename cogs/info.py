import discord
from discord.ext import commands
import asyncio
import json
from datetime import datetime, timedelta

class Info(commands.Cog):
    '''
    Verious informational commands
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Cog "{}" has been loaded!'.format(self.__class__.__name__))

    @commands.command()
    async def serverinfo(self, ctx):
        '''
        Sends a list of information on the server
        '''
        icon_url = ctx.guild.icon_url
        members = set(ctx.guild.members)
        offline = filter(lambda m: m.status is discord.Status.offline, members)
        offline = set(offline)
        bots = filter(lambda m: m.bot, members)
        bots = set(bots)
        users = members - bots
        server_created_at = ("{}".format(ctx.guild.created_at.strftime("%d %b %Y %H:%M")))
        embed = discord.Embed(title="Server Info", colour=0xf47fb1)
        embed.set_thumbnail(url=icon_url)
        embed.description = "Here's a bit of information on the server!"
        embed.add_field(name="Server Name", value=str(ctx.guild.name))
        embed.add_field(name="Server ID", value=str(ctx.guild.id))
        embed.add_field(name="Server Region", value=str(ctx.guild.region))
        embed.add_field(name="Server Verification", value=str(ctx.guild.verification_level))
        embed.add_field(name="Server Created At", value=str(server_created_at))
        embed.add_field(name="Server Roles", value=str(len(ctx.guild.roles) - 1))
        embed.add_field(name="Total Bots", value=str(len(bots)))
        embed.add_field(name="Bots Online", value=str(len(bots - offline)))
        embed.add_field(name="Bots Offline", value=str(len(bots & offline)))
        embed.add_field(name="Total Users", value=str(len(users)))
        embed.add_field(name="Online Users", value=str(len(users - offline)))
        embed.add_field(name="Offline Users", value=str(len(users & offline)))
        embed.set_footer(text="Requested at {0} UTC±0 in channel #{1}".format(datetime.now().strftime('%H:%M:%S'), ctx.message.channel))
        await ctx.send(embed=embed)

    @commands.command()
    async def inrole(self, ctx, *, role: discord.Role):
        desc = ""
        embed = discord.Embed(title="Members with role {}".format(role.name), colour=0xf47fb1)
        for member in role.members:
            if member.nick != None:
                desc += "{} ({})\n".format(member.name, member.nick)
            else:
                desc += "{}\n".format(member.name)
        embed.description = desc
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
