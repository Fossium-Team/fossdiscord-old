import discord
from discord.ext import commands
import config
import globalconfig
import importlib
import subprocess
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def lockdownbot(self, ctx):
        """Locks down bot globally. Bot owner only."""
        if str(ctx.message.author.id) == config.ownerID:
            if config.bot_lockdown_status == 'no_lockdown':
                em = discord.Embed(title = "Bot Lockdown Activated", description = "This bot is now locked down. Most commands will not work in any server.")
                await ctx.send(embed = em)
                await self.bot.change_presence(activity=discord.Game(name='v' + globalconfig.version + " | LOCKED DOWN"))
                with open('./config.py', 'r') as file :
                    filedata = file.read()
                filedata = filedata.replace('no_lockdown', 'lockdown_activated')
                with open('./config.py', 'w') as file:
                    file.write(filedata)
                importlib.reload(config)
            elif config.bot_lockdown_status == 'lockdown_activated':
                em = discord.Embed(title = "Bot Lockdown Deactivated", description = "This bot is now unlocked. All commands will now work in any server.")
                await ctx.send(embed = em)
                await self.bot.change_presence(activity=discord.Game(name=''))
                with open('./config.py', 'r') as file :
                    filedata = file.read()
                filedata = filedata.replace('lockdown_activated', 'no_lockdown')
                with open('./config.py', 'w') as file:
                    file.write(filedata)
                importlib.reload(config)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.")
            await ctx.send(embed = em)

    @commands.command()
    async def reloadcog(self, ctx, *args):
        """Reloads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            args = "cogs." + " ".join(args[:])
            self.bot.unload_extension(args)
            self.bot.load_extension(args)
            em = discord.Embed(title = "Cog Reloaded", description = "`" + args + "` has been reloaded.")
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.")
            await ctx.send(embed = em)

    @commands.command()
    async def unloadcog(self, ctx, *args):
        """Unloads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            args = "cogs." + " ".join(args[:])
            self.bot.unload_extension(args)
            em = discord.Embed(title = "Cog Unloaded", description = "`" + args + "` has been unloaded.")
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.")
            await ctx.send(embed = em)

    @commands.command()
    async def loadcog(self, ctx, *args):
        """Loads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            args = "cogs." + " ".join(args[:])
            self.bot.load_extension(args)
            em = discord.Embed(title = "Cog Loaded", description = "`" + args + "` has been loaded.")
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.")
            await ctx.send(embed = em)

    @commands.command()
    async def restartbot(self, ctx):
        """Restarts the bot"""
        if str(ctx.message.author.id) == config.ownerID:
            first_embed = discord.Embed(title = "Restarting bot...")
            msg = await ctx.send(embed=first_embed)
            dir_path = os.getcwd()
            subprocess.Popen(['python3', dir_path + '/bot.py'])
            new_embed = discord.Embed(title = "Restarted bot!")
            await msg.edit(embed=new_embed)
            await ctx.bot.close()
        else:
            em = discord.Embed(title = "This command is for the bot owner only.")
            await ctx.send(embed = em)

    @commands.command()
    async def shutdownbot(self, ctx):
        """Shuts down the bot"""
        if str(ctx.message.author.id) == config.ownerID:
            first_embed = discord.Embed(title = "Shutting down bot...")
            msg = await ctx.send(embed=first_embed)
            new_embed = discord.Embed(title = "Shut down bot!", description = "Check your console, as it may still be running a subprocess. If it is, press `ctrl + c` on your keyboard to end the process.")
            await msg.edit(embed=new_embed)
            await ctx.bot.close()
        else:
            em = discord.Embed(title = "This command is for the bot owner only.")
            await ctx.send(embed = em)
        

    @commands.command()
    async def servers(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            servers = list(self.bot.guilds)
            embed = discord.Embed(title = f"Connected on {str(len(servers))} servers:")
            embed.add_field(name = "Servers", value = '\n'.join(guild.name for guild in self.bot.guilds))
            embed.add_field(name = "Server IDs", value = '\n'.join(str(guild.id) for guild in self.bot.guilds))
            #embed.add_field(name = "Server Invites", value = '\n'.join(for guild in self.bot.guilds: server = self.bot.get_guild(int(guild.id)); for channel in server.channels: invite = await channel.create_invite() if channel.name == "general"))
            await ctx.send(embed = embed)
            #await ctx.send(f"Connected on {str(len(servers))} servers:")
            #await ctx.send('\n'.join(guild.name for guild in self.bot.guilds))
        else:
            em = discord.Embed(title = "This command is for the bot owner only.")
            await ctx.send(embed = em)

    @commands.command()
    async def getinvite(self, ctx, serverID, channelName = None):
        if str(ctx.message.author.id) == config.ownerID:
            if channelName != None:
                channelQuery = channelName
            elif channelName == None:
                channelQuery = "general"
            server = self.bot.get_guild(int(serverID))
            #await ctx.send(server)
            embed = discord.Embed(title = f"Generated invite for '{server.name}'")
            #channel = discord.utils.get(server.channels, name='general')
            #await ctx.send(channel)
            for channel in server.channels:
                if channel.name.__contains__(channelQuery) == True:
                    #await ctx.send(channel.id)
                    embed.add_field(name = "Channel Name", value = channel.name)
                    embed.add_field(name = "Channel ID", value = channel.id)
                    invite = await channel.create_invite()
                    embed.add_field(name = "Channel Invite", value = invite)
                    await ctx.send(embed = embed)
                    break
                #invite = channel.create_invite()
                #await ctx.send(invite)
            #guildID = ctx
            #server = discord.utils.get(str(guildID))
            #channel = discord.utils.get(server.channels, name='General')
            #invite = channel.create_invite()
            #await ctx.send(invite)

    @commands.command()
    async def getchannels(self, ctx, serverID):
        if str(ctx.message.author.id) == config.ownerID:
            server = self.bot.get_guild(int(serverID))
            #await ctx.send(server)
            #channel = discord.utils.get(server.channels, name='general')
            #await ctx.send(channel)
            embed = discord.Embed(title = f"List of channels for the server '{server.name}'")
            for channel in server.channels:
                #channelsList.append(channel.name)
                embed.add_field(name = channel.name, value = channel.type)
            #channelslist = list(server.channels)
            #embed.add_field(name = "Servers", value = '\n'.join(str(channelslist)))
            await ctx.send(embed = embed)
            #for channel in server.channels:
                #await ctx.send(channel)
                #invite = channel.create_invite()
                #await ctx.send(invite)

    @commands.command()
    async def leaveserver(self, ctx, serverID):
        if str(ctx.message.author.id) == config.ownerID:
            server = self.bot.get_guild(int(serverID))
            await server.leave_server(server)
            embed = discord.Embed(title = f"Left the server '{server.name}'.")
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Admin(bot))
