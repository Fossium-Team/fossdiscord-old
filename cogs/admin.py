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

def setup(bot):
    bot.add_cog(Admin(bot))
