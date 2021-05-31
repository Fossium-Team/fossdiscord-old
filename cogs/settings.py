# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import os
import sys
import asyncio
sys.path.append(os.path.realpath('.'))
import config

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def botstatus(self, ctx, *args):
        """Sets the status of the bot. Owner only. 'botstatus' to reset"""
        args = " ".join(args[:])
        if str(ctx.message.author.id) == config.ownerID:
            if args == '':
                await self.bot.change_presence(activity=discord.Game(name=''))

                em = discord.Embed(title = "Bot status successfully reset!", color = discord.Color.green())
                await ctx.send(embed = em)
            else:
                await self.bot.change_presence(activity=discord.Game(name=args))

                em = discord.Embed(title = "Bot status successfully changed to `" + args + "`!", color = discord.Color.green())
                await ctx.send(embed = em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)


    @commands.command()
    async def botstatusrepeat(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            em = discord.Embed(title = "Status loop initiated.", color = discord.Color.orange())
            await ctx.send(embed = em)

            while True:
                #Here is the template for setting changing FreeDiscord now playing status automatically:
                #await self.bot.change_presence(activity=discord.Game("made by the FreeTechnologies team"))
                #await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Made by the FreeTechnologies team! | https://discord.gg/QhhUVy92ZK"))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Visual Studio Code"))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Atom Editor"))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Fixing Bugs..."))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Publishing Releases..."))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("v0.6 | " + config.prefix + "help"))
                await asyncio.sleep(10)
        else:
            em = discord.Embed(title = "This command is for the bot owner only!")
            await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Settings(bot))
