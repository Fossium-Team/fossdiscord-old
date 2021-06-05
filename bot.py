# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import config
import globalconfig
import socket

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
    await bot.change_presence(activity=discord.Game(name='v' + globalconfig.version + " | " + config.prefix + "help"))
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
bot.load_extension("cogs.vt_scan")
bot.load_extension("cogs.fun")

@bot.event
async def on_message(msg):
    # if str(msg.author.id) in config.blacklist:
    #     for command in globalconfig.commands:
    #         if msg.content.__contains__(str(command)):
    #             BotOwner = await bot.fetch_user(config.ownerID)
    #             em = discord.Embed(title = "User Blacklisted", description = f"You are blacklisted from using the bot. Please contact {BotOwner} for more information.")
    #             await msg.channel.send(embed = em, delete_after=10.0)
    #             return
    
    # check for bad words
    for word in config.bad_words:
        if word in msg.content.lower():
            await msg.delete()
            await msg.channel.send("Please don't use that word", delete_after=5.0, color = discord.Color.orange())
        else:
            await bot.process_commands(msg)

    await bot.process_commands(msg)

# error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        em = discord.Embed(title = "Error", description = "You do not have permission to do that.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)
    elif isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title = "Error", description = "Your command is missing an argument.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)
    elif isinstance(error, commands.CommandNotFound):
        em = discord.Embed(title = "Error", description = "Command not found", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)
    else:
        em = discord.Embed(title = "An internal error occurred.", color = discord.Color.red())
        em.add_field(name = "Detailed Error", value = "`" + str(error) + "`")
        await ctx.send(embed = em)

# multi-instances prevention
def bind():
    host = "127.0.0.1"
    port = 18265
    _socket = socket.socket()
    _socket.bind((host,port))
    _socket.listen(1)
    conn, addr = _socket.accept()
    while True:
            data = conn.recv(1024).decode()
            if str(data) == 'disconnect':
                    print('Disconnect signal received, disconnecting...')
                    _socket.close()
                    break

try:
    bind()
except Exception as e:
    print('Something went wrong, probably there is another instance running.')
    print(e)
    quit()
try:
    bot.run(config.bot_token)
except Exception as e:
    message = 'disconnect'
    host = '127.0.0.1'
    port = 18265
    _socket = socket.socket()
    _socket.connect((host,port))
    _socket.send(message.encode())
    _socket.close()
    print(e)
    quit()