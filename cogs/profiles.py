import discord
from discord.ext import commands
import json
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import requests
from io import BytesIO

def retrieve_balance(id):
    with open("data/wallets.json", "r") as f:
        wallets = json.load(f)
    return(wallets[id])

class Profiles(commands.Cog):
    """
    User profiles
    """
    def __init__(self, bot):
        self.bot = bot
        print('Cog "{}" has been loaded!'.format(self.__class__.__name__))

    @commands.command(aliases=["userinfo"])
    async def profile(self, ctx, *, user : discord.Member = None):
        async with ctx.channel.typing():
            if user == None:
                user = ctx.message.author
            try:
                walletval = str(retrieve_balance(str(user.id)))
            except:
                walletval = '0'
            if user.status == discord.Status.online:
                fillclr = (67, 181, 129, 255)
            elif user.status == discord.Status.idle:
                fillclr = (250, 166, 26, 255)
            elif user.status == discord.Status.dnd:
                fillclr =  (240, 71, 71, 255)
            elif user.status == discord.Status.offline:
                fillclr = (116, 127, 141, 255)
            else:
                fillclr = "purple"
            nickname = user.nick
            if nickname == None:
                nickname = "No nickname"
            id = str(user.id)
            avatar = requests.get(user.avatar_url)
            avatar = Image.open(BytesIO(avatar.content))
            basewidth = 156
            wpercent = (basewidth / float(avatar.size[0]))
            hsize = int((float(avatar.size[1]) * float(wpercent)))
            avatar = avatar.resize((basewidth, hsize), Image.ANTIALIAS)
            avatar.save('data/tempavatar.png')
            pfp = Image.open('data/tempavatar.png')
            im = Image.open('data/pfcard.png')
            im.paste(pfp, (12, 91))
            draw = ImageDraw.Draw(im)
            draw.ellipse((172, 65, 189, 81), fill = fillclr, outline = fillclr)
            font = ImageFont.truetype('data/fonts/Montserrat-SemiBold.ttf', 30)
            draw.text((177, 90), user.name, (255, 255, 255), font=font)
            font = ImageFont.truetype('data/fonts/Montserrat-SemiBold.ttf', 20)
            draw.text((177, 159), nickname, (243, 70, 183), font=font)
            draw.text((177, 214), id, (243, 70, 183), font=font)
            draw.text((297, 248), str(user.top_role), (243, 70, 183), font=font)
            draw.text((276, 290), user.joined_at.strftime('%a, %b %d, %Y'), (243, 70, 183), font=font)
            font = ImageFont.truetype('data/fonts/Montserrat-SemiBold.ttf', 35)
            draw.text((68, 260), walletval, (243, 70, 183), font=font)
            im.save(f'data/profile_{user.id}.png')
            await ctx.send(file = discord.File(f'data/profile_{user.id}.png'))
            os.remove(f'data/profile_{user.id}.png')
            os.remove('data/tempavatar.png')

def setup(bot):
    bot.add_cog(Profiles(bot))
