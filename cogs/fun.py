import discord
from discord.ext import commands
import json
from datetime import datetime
import random

def parser(message):
    return(message[message.find(' ')+1:])

class Fun(commands.Cog):
    """
    Fun stuff
    """
    def __init__(self, bot):
        self.bot = bot
        print('Cog "{}" has been loaded!'.format(self.__class__.__name__))

    @commands.command(pass_context=True, brief="Gain 150 credits once per day")
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        '''
        Adds 150 to your balance once per day
        '''
        user = str(ctx.message.author.id)
        with open('data/wallets.json', 'r') as f:
            wallets = json.load(f)
        if user not in wallets:
            wallets[user] = 0
        wallets[user] += 150
        with open('data/wallets.json', 'w') as f:
            json.dump(wallets, f, indent=2)
        cur_balance = wallets[user]
        embed = discord.Embed(title="Wallet updated!", colour=0xf47fb1)
        embed.description = ":moneybag: Gained 150 credits! Your balance is now {}.".format(cur_balance)
        await ctx.send(embed=embed)

    @commands.command(aliases=["balance","credits"])
    async def wallet(self, ctx):
        '''
        Checks your credit balance
        '''
        user = str(ctx.message.author.id)
        with open('data/wallets.json', 'r') as f:
            wallets = json.load(f)
        if user not in wallets:
            wallets[user] = 0
        cur_balance = wallets[user]
        embed = discord.Embed(title="Current balance", colour=0xf47fb1)
        embed.description = ":moneybag: Your current balance is {}.".format(cur_balance)
        await ctx.send(embed=embed)

    @commands.has_permissions(ban_members=True)
    @commands.command(pass_context=True, hidden=True, aliases=['givecredit','gc'])
    async def givecredits(self, ctx, member: discord.Member, amount=0):
        '''
        Gives x amount of credits to another person
        '''
        member = str(member.id)
        with open('data/wallets.json') as f:
            wallets = json.load(f)
        if member not in wallets:
            wallets[member] = 0
        balance = int(wallets[member]) + amount
        wallets[member] = balance
        with open('data/wallets.json', 'w') as f:
            json.dump(wallets, f, indent=2, sort_keys=True)
        embed = discord.Embed(title="You've been given credits!~", colour=0xf47fb1)
        embed.description = "Your balance is now {} after being given {} credits.".format(balance, amount)
        await ctx.send(embed=embed)

    @commands.command(aliases=["cf","coin","flip"])
    async def coinflip(self, ctx):
        await ctx.send(random.choice(["Heads!","Tails!"]))

    @commands.command(pass_context=True, brief='Says something')
    async def say(self, ctx, *, string=""):
        await ctx.message.delete()
        string = string.replace('@everyone', '`@everyone`').replace('@here', '`@here`')
        await ctx.send("{}".format(string))

def setup(bot):
    bot.add_cog(Fun(bot))
