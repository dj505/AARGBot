import discord
import json
import os
from discord.ext import commands

with open("configs/config.json", "r") as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=config["prefix"])

failed_addons = []
for i in os.listdir("cogs"):
    if i.endswith(".py"):
        try:
            if ".py" in i:
                i = i.replace(".py","")
            bot.load_extension("cogs.{}".format(i))
        except Exception as e:
            print("Failed to add cog {}!".format(i))
            print(e)
    else:
        print("Ignoring file/folder {}...".format(i))

temp_vars = {}
if len(failed_addons) > 0:
    temp_vars["failed_addons"] = failed_addons
else:
    temp_vars["failed_addons"] = "None"

with open("configs/temp_vars.json", "w") as f:
    json.dump(temp_vars, f, indent=2)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        try:
            bot.guild = guild
            bot.creator = discord.utils.get(guild.members, id=config["bot_creator"])
            bot.log_channel = discord.utils.get(guild.channels, id=config["log_channel"])
            bot.welcome_channel = discord.utils.get(guild.channels, id=config["welcome_channel"])
            bot.admin_role = discord.utils.get(guild.roles, id=config["admin_role"])
            bot.mod_role = discord.utils.get(guild.roles, id=config["mod_role"])
        except Exception as e:
            print("There was an error assigning channel and/or role variables.")
            print(e)

    print("Up and running as {0.user}!".format(bot))
    print("Prefix is {}".format(config["prefix"]))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(config["status"]))

bot.run(config["token"])
