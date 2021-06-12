# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import os
import sys
import asyncio
sys.path.append(os.path.realpath('.'))
import config
import json

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
            em = discord.Embed(title = "Status loop initiated.", color = discord.Color.green())
            await ctx.send(embed = em)

            while True:
                await self.bot.change_presence(activity=discord.Game("Made by the FOSS-Devs team!"))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Visual Studio Code"))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Atom Editor"))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Fixing Bugs..."))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Publishing Releases..."))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game(f"{globalconfig.currentversion} | {config.prefix}help"))
                await asyncio.sleep(10)
        else:
            em = discord.Embed(title = "This command is for the bot owner only!", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.group(invoke_without_command=True)
    async def blacklist(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            em = discord.Embed(title = 'Arguments:', color = discord.Color.blue())
            em.add_field(name = f"{config.prefix}blacklist add (userid)", value="Add a user to the blacklist.")
            em.add_field(name = f"{config.prefix}blacklist remove (userid)", value="Remove a user from the blacklist.")
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only!", color = discord.Color.red())
            await ctx.send(embed = em)

    @blacklist.command(name="add")
    async def _add(self, ctx, userid):
        if str(ctx.message.author.id) == config.ownerID:
            if not os.path.exists('settings'):
                os.makedirs('settings')
            try:
                if os.stat("settings/blacklist.json").st_size > 0:
                    lst = []
                    with open("settings/blacklist.json") as file:
                        blacklistjson = json.load(file)
                    for attr, value in blacklistjson['data']:
                        lst.append(attr)
                    usernum = str(lst[-1])
                    usernum = int(''.join(filter(str.isdigit, str(usernum)))) + 1
                    writeblacklist = blacklistjson.update({f'user{usernum}': f'{userid}'})
                    #blacklisted = blacklistjson['blacklist']
                    #blacklist = f'{blacklisted}, {userid}'
                    #riteblacklist = ({"blacklist": f'{blacklist}'})
                    with open("settings/blacklist.json", 'w') as file:
                        json.dump(writeblacklist, file)
                    em = discord.Embed(title = 'Blacklisted that user.', color = discord.Color.green())
                    await ctx.send(embed=em)
                
                elif os.stat("settings/blacklist.json").st_size == 0:
                    writeblacklist = {"user0": userid}
                    with open("settings/blacklist.json", 'w') as file:
                        json.dump(writeblacklist, file)
                    em = discord.Embed(title = 'Blacklisted that user.', color = discord.Color.green())
                    await ctx.send(embed=em)

            except:
                writeblacklist = {"user0": userid}
                with open("settings/blacklist.json", 'w') as file:
                    json.dump(writeblacklist, file)
                em = discord.Embed(title = 'Blacklisted that user.', color = discord.Color.green())
                await ctx.send(embed=em)

        else:
            em = discord.Embed(title = "This command is for the bot owner only!", color = discord.Color.red())
            await ctx.send(embed = em)

    # @blacklist.command(name="remove")
    # async def _remove(self, ctx, userid):
    #     if str(ctx.message.author.id) == config.ownerID:
    #         if not os.path.exists('settings'):
    #             os.makedirs('settings')
    #         try:
    #             if os.stat("settings/blacklist.json").st_size > 0:
    #                 with open("settings/blacklist.json") as file:
    #                     blacklistjson = json.load(file)
    #                 blacklisted = blacklistjson['blacklist']
    #                 
    #                 blacklistjson.pop('hours', None)
    #                 
    #                 blacklist = blacklisted.replace(f'{userid}, ')
    #                 writeblacklist = {"blacklist": blacklist}
    #                 with open("settings/blacklist.json", 'w') as file:
    #                     json.dump(writeblacklist, file)
    #                 em = discord.Embed(title = 'Removed that user from the blacklist.', color = discord.Color.green())
    #                 await ctx.send(embed=em)
                
    #             elif os.stat("settings/blacklist.json").st_size == 0:
    #                 em = discord.Embed(title = 'Nobody is blacklisted yet.', color = discord.Color.red())
    #                 await ctx.send(embed=em)

    #         except:
    #             em = discord.Embed(title = 'Nobody is blacklisted yet.', color = discord.Color.red())
    #             await ctx.send(embed=em)
    #     else:
    #         em = discord.Embed(title = "This command is for the bot owner only!", color = discord.Color.red())
    #         await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(Settings(bot))
