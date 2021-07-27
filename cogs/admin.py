# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import config
import globalconfig
import importlib
import subprocess
import os
import sys

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reloadcog(self, ctx, *cog):
        """Reloads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            if not cog:
                em = discord.Embed(title = 'The argument `cog` is missing', color = discord.Color.red())
                await ctx.send(embed = em)
                return
            cog = "cogs." + " ".join(cog[:])
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
            em = discord.Embed(title = "Cog Reloaded", description = "`" + cog + "` has been reloaded", color = discord.Color.green())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def unloadcog(self, ctx, *cog):
        """Unloads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            if not cog:
                em = discord.Embed(title = 'The argument `cog` is missing', color = discord.Color.red())
                await ctx.send(embed = em)
                return
            cog = "cogs." + " ".join(cog[:])
            self.bot.unload_extension(cog)
            em = discord.Embed(title = "Cog Unloaded", description = "`" + cog + "` has been unloaded", color = discord.Color.green())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def loadcog(self, ctx, *cog):
        """Loads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            if not cog:
                em = discord.Embed(title = 'The argument `cog` is missing', color = discord.Color.red())
                await ctx.send(embed = em)
                return
            cog = "cogs." + " ".join(cog[:])
            self.bot.load_extension(cog)
            em = discord.Embed(title = "Cog Loaded", description = "`" + cog + "` has been loaded", color = discord.Color.green())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def shutdownbot(self, ctx):
        """Shuts down the bot"""
        if str(ctx.message.author.id) == config.ownerID:
            first_embed = discord.Embed(title = "Shutting down bot...", color = discord.Color.orange())
            msg = await ctx.send(embed=first_embed)
            new_embed = discord.Embed(title = "The bot is shut down!", description = "Check your console, as it may still be running. If it is, press `ctrl + c` on your keyboard to end the process", color = discord.Color.green())
            await msg.edit(embed=new_embed)
            await ctx.bot.close()
        else:
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def restartbot(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            first_embed = discord.Embed(title = "Restarting bot...", color = discord.Color.orange())
            msg = await ctx.send(embed=first_embed)
            new_embed = discord.Embed(title = "The bot has restarted!", color = discord.Color.green())
            #close_port()
            await msg.edit(embed=new_embed)
            await ctx.bot.close()
            subprocess.Popen([sys.executable, "bot.py"]) 
        else:
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def servers(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            servers = list(self.bot.guilds)
            embed = discord.Embed(title = f"Connected on {str(len(servers))} servers:", color = discord.Color.green())
            embed.add_field(name = "Servers", value = '\n'.join(guild.name for guild in self.bot.guilds))
            embed.add_field(name = "Server IDs", value = '\n'.join(str(guild.id) for guild in self.bot.guilds))
            #embed.add_field(name = "Server Invites", value = '\n'.join(for guild in self.bot.guilds: server = self.bot.get_guild(int(guild.id)); for channel in server.channels: invite = await channel.create_invite() if channel.name == "general"))
            await ctx.send(embed = embed)
            #await ctx.send(f"Connected on {str(len(servers))} servers:")
            #await ctx.send('\n'.join(guild.name for guild in self.bot.guilds))
        else:
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def getinvite(self, ctx, serverID = None, channelName = None):
        if str(ctx.message.author.id) == config.ownerID:
            if serverID is None:
                em = discord.Embed(title = 'The argument `serverID` is missing', color = discord.Color.red())
                await ctx.send(embed = em)
                return
            if channelName != None:
                channelQuery = channelName
            elif channelName == None:
                channelQuery = "general"
            server = self.bot.get_guild(int(serverID))
            #await ctx.send(server)
            embed = discord.Embed(title = f"Generated invite for '{server.name}'", color = discord.Color.green())
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
        else:
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def getchannels(self, ctx, serverID = None):
        if str(ctx.message.author.id) == config.ownerID:
            if serverID is None:
                em = discord.Embed(title = 'The argument `serverID` is missing', color = discord.Color.red())
                await ctx.send(embed = em)
                return
            server = self.bot.get_guild(int(serverID))
            #await ctx.send(server)
            #channel = discord.utils.get(server.channels, name='general')
            #await ctx.send(channel)
            embed = discord.Embed(title = f"List of channels for the server '{server.name}'", color = discord.Color.green())
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
        else:
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def leaveserver(self, ctx, serverID = None):
        if str(ctx.message.author.id) == config.ownerID:
            if serverID is None:
                em = discord.Embed(title = 'The argument `serverID` is missing', color = discord.Color.red())
                await ctx.send(embed = em)
                return
            server = self.bot.get_guild(int(serverID))
            await server.leave()
            embed = discord.Embed(title = f"Left the server '{server.name}'", color = discord.Color.green())
            await ctx.send(embed = embed)
        else:
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
            await ctx.send(embed = em)
    
def setup(bot):
    bot.add_cog(Admin(bot))
