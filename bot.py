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
from datetime import datetime
from better_profanity import profanity

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
async def on_message(message):
    if not os.path.exists('settings'):
        os.makedirs('settings')
    if message.channel.type is discord.ChannelType.private:
        pass
    else:
        try:
            with open(f"settings/enablement-{message.guild.id}.json") as file:
                data = json.load(file)
            command_enable = data["settings"]["commands"]
            filter_enable = data["settings"]["filter"]
        except Exception:
            default = {"settings": {"filter": 1, "commands": 1}}
            with open(f"settings/enablement-{message.guild.id}.json", 'w') as file:
                data = json.dump(default, file)
            filter_enable = 1
            command_enable = 1
        if filter_enable == 1:
            #Check for profanity.
            if profanity.contains_profanity(message.content) == True:
                await message.delete()
                em = discord.Embed(title = "Please don't use that sort of language", color = discord.Color.orange())
                await message.channel.send(embed=em, delete_after=10.0)
                if not os.path.exists('settings'):
                    os.makedirs('settings')
                if os.path.isfile(f"settings/logging-{message.guild.id}.json"):
                    with open(f"settings/logging-{message.guild.id}.json") as file:
                        loggingjson = json.load(file)
                    loggingchannel = loggingjson["data"]["logging"]["channel"]
                    channel = bot.get_channel(int(loggingchannel))
                    em = discord.Embed(title = f"{message.author} used swear word(s)", color = discord.Color.red())
                    em.set_author(name=message.author, icon_url=message.author.avatar_url)
                    em.add_field(name = "Message", value = message.content)

                    if os.path.isfile(f"settings/dateformat-{message.guild.id}.json"):
                        with open(f"settings/dateformat-{message.guild.id}.json") as file:
                            dateformatjson = json.load(file)
                        date_format = dateformatjson["data"]["dateformat"]["format"]
                    else:
                        date_format = config.date_format

                    datetimenow = datetime.now()
                    currentdate = datetime.strftime(datetimenow, date_format)
                    em.set_footer(text = f"{currentdate}")
                    await channel.send(embed=em)
                else:
                    return
            else:
                pass
        else:
            pass

        if os.path.isfile(f"settings/blacklist.json"):
            with open(f"settings/blacklist.json") as file:
                blacklistjson = json.load(file)
            blacklist = blacklistjson["data"]
            if blacklist == {}:
                pass
            else:
                for attr, value in blacklist.items():
                    if re.search(str(message.author.id), blacklist[attr]["id"]):
                        if re.match(f'{config.prefix}', message.content):
                            BotOwner = await bot.fetch_user(config.ownerID)
                            em = discord.Embed(title = "You Are Blacklisted", description = f"You are blacklisted from using the bot. Please contact {BotOwner} for more information.", color = discord.Color.red())
                            await message.channel.send(embed = em, delete_after=10.0)
                            return
                        else:
                            pass
                    else:
                        pass
        else:
            pass
        if command_enable == 1:
            await bot.process_commands(message)
        else:
            if f"{config.prefix}settings" in message.content or f"{config.prefix}shutdownbot" in message.content:
                await bot.process_commands(message)
            elif f"{config.prefix}restartbot" in message.content:
                await bot.process_commands(message)
            else:
                pass

# error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.message.delete()
        em = discord.Embed(title = "Error", description = "You do not have permission to do that.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em, delete_after=10.0)
    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title = "Error", description = "Your command is missing an argument.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em, delete_after=10.0)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.message.delete()
        em = discord.Embed(title = "Error", description = "Command not found.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em, delete_after=10.0)
    elif isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in `{round(error.retry_after*1)}s`.", color = discord.Color.red())
        await ctx.send(embed=em, delete_after=10.0)
    elif isinstance(error, commands.MaxConcurrencyReached):
        await ctx.message.delete()
        em = discord.Embed(title=f"Oops!", description="Someone on this server is using this command, please wait.", color = discord.Color.red())
        await ctx.send(embed=em, delete_after=10.0)
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
        print('Bind port failed, probably another bot instance is running.')
        quit()
    bot.run(config.bot_token)

start()
