import discord
from discord.ext import commands
import asyncio
from datetime import datetime, timedelta
import json
import random

class Events(commands.Cog):
    '''
    Logging of messages and actions
    '''
    def __init__(self, bot):
        self.bot = bot
        print('Cog "{}" has been loaded!'.format(self.__class__.__name__))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_msgs = [f'Welcome to AARG, {member.name}!', f'Sup, {member.name}?', f'Hey {member.name}, welcome to AARG!', f'{member.name} is here! Welcome!']
        embed = discord.Embed(title="Member Joined", color=0x81FF47)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=None, value="{0.name}#{0.discriminator} joined the server.".format(member))
        await self.bot.log_channel.send(embed=embed)
        await self.bot.welcome_channel.send(random.choice(welcome_msgs))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="Member Left Or Was Kicked", color=0xFF6647)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=None, value="{0.name}#{0.discriminator} left the server or was kicked.".format(member))
        await self.bot.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.pinned != after.pinned:
            # I don't think this works yet
            if after.pinned == True:
                pin_state = "pinned"
            else:
                pin_state = "unpinned"
            embed = discord.Embed(title="Message {} in #{}".format(pin_state, after.channel), description=after.content, color=0xFFCB5B)
            embed.add_field(name="Message:", value=after.content)
            await self.bot.log_channel.send(embed=embed)
        if before.content != after.content:
            # This works fine
            embed = discord.Embed(title="Message by {} edited in #{}".format(before.author.name, before.channel.name), color=0xFFCB5B)
            embed.set_thumbnail(url=before.author.avatar_url)
            embed.add_field(name="Before:", value=before.content, inline=False)
            embed.add_field(name="After:", value=after.content, inline=False)
            await self.bot.log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel != self.bot.log_channel and !message.content.startswith('--say'):
            embed = discord.Embed(title="Message by {} deleted in #{}".format(message.author.name, message.channel.name), color=0xFF6647)
            embed.set_thumbnail(url=message.author.avatar_url)
            embed.add_field(name="Message:", value=message.content, inline=False)
            await self.bot.log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))
