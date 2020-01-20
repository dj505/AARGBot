import discord
from discord.ext import commands
import asyncio
import json
from datetime import datetime, timedelta
import random

class Admin(commands.Cog):
    '''
    Admin tools
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Cog "{}" has been loaded!'.format(self.__class__.__name__))

    @commands.command()
    async def test(self, ctx):
        '''
        To ensure various aspects of the bot are working right
        ''' # super janky but hey it has its uses
        with open("configs/temp_vars.json", "r") as f:
            temp_vars = json.load(f)
        embed = discord.Embed(title="Juice Bot Self Test", colour=0xf47fb1)
        embed.description = "Self test results for Juice Bot! Hopefully I'm working well~"
        embed.add_field(name="Online?", value=random.choice(["Nah", "Totally not", "Maybe?", "Perhaps", "Yeah", "I think so"]))
        if "None" not in temp_vars["failed_addons"]:
            failed_list = temp_vars["failed_addons"].split(", ")
        else:
            failed_list = "All addons running!"
        embed.add_field(name="Failed addons", value=failed_list)
        embed.set_footer(text="Test complete at {0} UTC±0 in channel #{1}".format(datetime.now().strftime('%H:%M:%S'), ctx.message.channel))
        await ctx.send(embed=embed)

    @commands.has_permissions(administrator = True)
    @commands.command(alias=["presence", "game"])
    async def status(self, ctx, game):
        '''
        Sets the bot's "Playing" status
        '''
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(game))
        embed = discord.Embed(title="Status changed!", colour=0xf47fb1)
        embed.description = "New status set!"
        embed.add_field(name="Status", value=game)
        with open("configs/config.json", "r") as f:
            settings = json.load(f)
            settings["status"] = game
        with open("configs/config.json", "w") as f:
            json.dump(settings, f, indent=2)
        await ctx.send(embed=embed)

    @commands.has_permissions(mention_everyone = True)
    @commands.command(aliases=["randommem", "pickmem", "someone"])
    async def randommember(self, ctx):
        '''
        Picks a random member from the server
        '''
        embed = discord.Embed(title="Picked a random member", colour=0xf47fb1)
        embed.description = random.choice(ctx.guild.members).mention
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))
