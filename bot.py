# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import config
import globalconfig
import socket
import os
import json
import re
import time

intents = discord.Intents.default()
intents.members = True

description = ""

bot = commands.Bot(command_prefix=config.prefix, description=description, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    # What gets printed in the terminal when the bot is succesfully logged in
    print('\n')
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("REMEMBER: YOU MUST RUN THE COMMAND '" + config.prefix + "shutdownbot' TO SHUTDOWN THE BOT!!!!")
    print('------')
    # Changes bot status to the default status when the bot starts up
    await bot.change_presence(activity=discord.Game(name=f'v{globalconfig.currentversion} | {config.prefix}help'))
    botowner = bot.get_user(int(config.ownerID))
    em = discord.Embed(title = "The bot is back online", color = discord.Color.green())
    await botowner.send(embed = em)

bot.load_extension("cogs.general")
bot.load_extension("cogs.utils")
bot.load_extension("cogs.moderation")
bot.load_extension("cogs.settings")
bot.load_extension("cogs.caesarcrypt")
bot.load_extension("cogs.help")
bot.load_extension("cogs.update")
bot.load_extension("cogs.admin")
bot.load_extension("cogs.vtscan")
bot.load_extension("cogs.fun")

@bot.event
async def on_message(msg):
    if not os.path.exists('settings'):
        os.makedirs('settings')
    if os.path.isfile(f"settings/blacklist.json"):
        with open(f"settings/blacklist.json") as file:
            blacklistjson = json.load(file)
        blacklisted = blacklistjson['blacklist']
        if re.search(str(msg.author.id), str(blacklisted)):
            for command in globalconfig.commands:
                if msg.content.__contains__(str(command)):
                        BotOwner = await bot.fetch_user(config.ownerID)
                        em = discord.Embed(title = "You Are Blacklisted", description = f"You are blacklisted from using the bot. Please contact {BotOwner} for more information.")
                        await msg.channel.send(embed = em, delete_after=10.0)
                        return
        else:
            await bot.process_commands(msg)
    else:
        await bot.process_commands(msg)
    
    # check for bad words
    for word in config.bad_words:
        if word in msg.content.lower():
            await msg.delete()
            await msg.channel.send("Please don't use that word", delete_after=5.0, color = discord.Color.orange())
        else:
            await bot.process_commands(msg)

# error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title = "Error", description = "You do not have permission to do that.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em, delete_after=10.0)
    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title = "Error", description = "Your command is missing an argument.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em, delete_after=10.0)
    elif isinstance(error, commands.CommandNotFound):
        em = discord.Embed(title = "Error", description = "Command not found", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em, delete_after=10.0)
    elif isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slowdown!", description=f"Try again in `{round(error.retry_after*1)}s`.", color = discord.Color.red())
        await ctx.send(embed=em, delete_after=10.0)
    elif isinstance(error, commands.MaxConcurrencyReached):
        await ctx.send(embed=em, delete_after=10.0)
        em = discord.Embed(title=f"Oops!", description="Someone on this server is using this command, please wait.", color = discord.Color.red())
        await ctx.message.delete()
    else:
        em = discord.Embed(title = "An internal error occurred.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)

# multi-instances prevention
def start():
    host = "127.0.0.1"
    port = 18265
    _socket = socket.socket()
    try:
        _socket.bind((host,port))
    except Exception as e:
        print(e)
        print('Bind port failed, probably another instance is running.')
        quit()
    bot.run(config.bot_token)


start()
