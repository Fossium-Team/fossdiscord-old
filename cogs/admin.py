# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
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
    async def reloadcog(self, ctx, *args):
        """Reloads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            args = "cogs." + " ".join(args[:])
            self.bot.unload_extension(args)
            self.bot.load_extension(args)
            em = discord.Embed(title = "Cog Reloaded", description = "`" + args + "` has been reloaded.", color = discord.Color.green())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def unloadcog(self, ctx, *args):
        """Unloads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            args = "cogs." + " ".join(args[:])
            self.bot.unload_extension(args)
            em = discord.Embed(title = "Cog Unloaded", description = "`" + args + "` has been unloaded.", color = discord.Color.green())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def loadcog(self, ctx, *args):
        """Loads a cog"""
        if str(ctx.message.author.id) == config.ownerID:
            args = "cogs." + " ".join(args[:])
            self.bot.load_extension(args)
            em = discord.Embed(title = "Cog Loaded", description = "`" + args + "` has been loaded.", color = discord.Color.green())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def shutdownbot(self, ctx):
        """Shuts down the bot"""
        if str(ctx.message.author.id) == config.ownerID:
            first_embed = discord.Embed(title = "Shutting down bot...", color = discord.Color.orange())
            msg = await ctx.send(embed=first_embed)
            new_embed = discord.Embed(title = "The bot is shut down!", description = "Check your console, as it may still be running a subprocess. If it is, press `ctrl + c` on your keyboard to end the process.", color = discord.Color.green())
            #close_port()
            await msg.edit(embed=new_embed)
            await ctx.bot.close()
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
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
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
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
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
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
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def getchannels(self, ctx, serverID):
        if str(ctx.message.author.id) == config.ownerID:
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
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def leaveserver(self, ctx, serverID):
        if str(ctx.message.author.id) == config.ownerID:
            server = self.bot.get_guild(int(serverID))
            await server.leave()
            embed = discord.Embed(title = f"Left the server '{server.name}'.", color = discord.Color.green())
            await ctx.send(embed = embed)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    # @commands.command()
    # async def blacklist(self, ctx, user : discord.Member):
    #     if str(ctx.message.author.id) == config.ownerID:
    #         with open("blacklist.py") as blacklistfilecheck:
    #             if str(user.id) in blacklistfilecheck:
    #                 em = discord.Embed(title = "That member is already blacklisted.", color = discord.Color.red())
    #             else:
    #                 await ctx.send("Successfully blacklisted that member.")
    #                 writeBlacklist = str(user.id)
    #                 blacklistfile = open("config/blacklist.py", 'a')
    #                 blacklistfile.write(writeBlacklist)
    #                 blacklistfile.close()
    #     else:
    #         em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
    #         await ctx.send(embed = em)

    # @commands.command()
    # async def delblacklist(self,ctx, user : discord.Member):
    #     if not os.path.exists('warns'):
    #         os.makedirs('warns')
    #     fn = "blacklist.py"
    #     f = open(fn)
    #     output = []
    #     word=str(user.id)
    #     for line in f:
    #         if not line.startswith(word):
    #             output.append(line)
    #     f.close()
    #     f = open(fn, 'w')
    #     f.writelines(output)
    #     f.close()
    #     em = discord.Embed(title = "Successfully removed the blacklist.", delete_after=10.0, color = discord.Color.green())
    
def setup(bot):
    bot.add_cog(Admin(bot))
