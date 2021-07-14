# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import os
import sys
import asyncio
import config
import json
import re

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
            em = discord.Embed(title = "This command is for the bot owner only", color = discord.Color.red())
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
                await self.bot.change_presence(activity=discord.Game("Fixing Bugs..."))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game("Publishing Releases..."))
                await asyncio.sleep(10)
                await self.bot.change_presence(activity=discord.Game(f'v{globalconfig.currentversion} | {config.prefix}help'))
                await asyncio.sleep(10)
        else:
            em = discord.Embed(title = "This command is for the bot owner only!", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.group(invoke_without_command=True)
    async def blacklist(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            em = discord.Embed(title = 'Arguments:', color = discord.Color.blue())
            em.add_field(name = f"{config.prefix}blacklist add <userid>", value="Add a user to the blacklist. Owner only.")
            em.add_field(name = f"{config.prefix}blacklist remove <userid>", value="Remove a user from the blacklist. Owner only.")
            await ctx.send(embed=em)
        else:
            em = discord.Embed(title = "This command is for the bot owner only!", color = discord.Color.red())
            await ctx.send(embed = em)

    @blacklist.command(name="add")
    async def _add(self, ctx, userid: str):
        if str(ctx.message.author.id) == config.ownerID:
            if not os.path.exists('settings'):
                os.makedirs('settings')
            try:
                if os.stat("settings/blacklist.json").st_size > 0:
                    lst = []
                    with open("settings/blacklist.json") as file:
                        blacklistjson = json.load(file)
                    blacklistitem = blacklistjson['data']
                    for attr, value in blacklistitem.items():
                        if str(userid) == blacklistitem[attr]["id"]:
                            em = discord.Embed(title = 'User is already in the blacklist', color = discord.Color.red())
                            await ctx.send(embed=em)
                            return
                        else:
                            pass
                    for attr, value in blacklistitem.items():
                        lst.append(attr)
                    usernum = str(lst[-1])
                    usernum = str(int(''.join(filter(str.isdigit, str(usernum)))) + 1)
                    blacklistjson["data"].update({f"user{usernum}": {"id": f'{userid}'}})
                    with open("settings/blacklist.json", 'w') as file:
                        json.dump(blacklistjson, file)
                    em = discord.Embed(title = 'Blacklisted that user', color = discord.Color.green())
                    await ctx.send(embed=em)
                
                elif os.stat("settings/blacklist.json").st_size == 0:
                    blacklistjson = {"data": {"user0": {"id":f'{userid}'}}}
                    with open("settings/blacklist.json", 'w') as file:
                        json.dump(blacklistjson, file)
                    em = discord.Embed(title = 'Blacklisted that user', color = discord.Color.green())
                    await ctx.send(embed=em)

            except FileNotFoundError:
                writeblacklist = {"data": {"user0": {"id":f'{userid}'}}}
                with open("settings/blacklist.json", 'w') as file:
                    json.dump(writeblacklist, file)
                em = discord.Embed(title = 'Blacklisted that user', color = discord.Color.green())
                await ctx.send(embed=em)

        else:
            em = discord.Embed(title = "This command is for the bot owner only!", color = discord.Color.red())
            await ctx.send(embed = em)

    @blacklist.command(name="remove")
    async def _remove(self, ctx, userid: str):
        if str(ctx.message.author.id) == config.ownerID:
            em = discord.Embed(title = 'Nobody is blacklisted yet', color = discord.Color.red())
            if not os.path.exists('settings'):
                os.makedirs('settings')
            if not os.path.isfile(f"settings/blacklist.json"):
                await ctx.send(embed=em)
                return
            if os.stat("settings/blacklist.json").st_size > 0:
                with open("settings/blacklist.json") as file:
                    blacklistjson = json.load(file)
                try:
                    blacklistitem = blacklistjson["data"]
                except NameError:
                    await ctx.send(embed=em)
                    return 
                if blacklistitem == {}:
                    await ctx.send(embed=em)
                    return
                else:
                    for attr, value in blacklistitem.items():
                        if blacklistitem[attr]["id"] == userid:
                            key_to_remove = attr
                            break
                    try:
                        del blacklistitem[key_to_remove]
                        with open("settings/blacklist.json", 'w') as file:
                            json.dump(blacklistjson, file)
                        em = discord.Embed(title = 'Removed that user from the blacklist', color = discord.Color.green())
                        await ctx.send(embed=em)
                    except NameError:
                        em = discord.Embed(title = 'User is not in blacklist', color = discord.Color.red())
                        await ctx.send(embed=em)
                
            elif os.stat("settings/blacklist.json").st_size == 0:
                await ctx.send(embed=em)


        else:
            em = discord.Embed(title = "This command is for the bot owner only!", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def settings(self, ctx):
        em = discord.Embed(title = 'Arguments:', color = discord.Color.blue())
        em.add_field(name = f"{config.prefix}settings logging <channelID or off>", value="Set a logging channel.")
        em.add_field(name = f"{config.prefix}settings dateformat", value="Set the date format used in the current guild.", inline = False)
        em.add_field(name = f"{config.prefix}settings filter <on or off>", value="Turn the filter on or off.")
        em.add_field(name = f"{config.prefix}settings filter <add or remove>", value="Add or remove words to the filter.")
        await ctx.send(embed=em)

    @settings.command(name="logging")
    @commands.has_permissions(administrator=True)
    async def _logging(self, ctx, *channel):
        channel = " ".join(channel[:])
        if not os.path.exists('settings'):
            os.makedirs('settings')
        if channel.lower() == "off":
            try:
                os.remove(f"settings/logging-{ctx.guild.id}.json")
                em = discord.Embed(title = 'Disabled logging.', color = discord.Color.green())
                await ctx.send(embed=em)
            except FileNotFoundError:
                em = discord.Embed(title = 'Logging was already disabled', color = discord.Color.red())
                await ctx.send(embed=em)
        elif not channel:
            em = discord.Embed(title = 'Please pass a valid argument', color = discord.Color.red())
            await ctx.send(embed=em)
        else:
            try:
                channeltest = self.bot.get_channel(int(channel))
                pass
            except Exception:
                em = discord.Embed(title = 'Please pass a valid argument', color = discord.Color.red())
                await ctx.send(embed=em)
                return
            if channeltest is None:
                em = discord.Embed(title = "That channel doesn't exist", color = discord.Color.red())
                await ctx.send(embed=em)
            else:
                try:
                    writelogging = {"data": {"logging": {"channel":f'{channel}'}}}
                    with open(f"settings/logging-{ctx.guild.id}.json", 'w') as file:
                        json.dump(writelogging, file)
                    em = discord.Embed(title = 'Set that channel as the logging channel', color = discord.Color.green())
                    await ctx.send(embed=em)

                except FileNotFoundError:
                    writelogging = {"data": {"logging": {"channel":f'{channel}'}}}
                    with open(f"settings/logging-{ctx.guild.id}.json", 'w') as file:
                        json.dump(writelogging, file)
                    em = discord.Embed(title = 'Set that channel as the logging channel', color = discord.Color.green())
                    await ctx.send(embed=em)

    @settings.command(name="dateformat")
    @commands.has_permissions(administrator=True)
    async def _dateformat(self, ctx):
        em = discord.Embed(title = "Choose the date format you want", color = discord.Color.blue())
        em.add_field(name = "Date formats:", value = "1️⃣ - day/month/year hour:minutes AM/PM\n2️⃣ - month/day/year hour:minutes AM/PM\n3️⃣ - day/month/year hour:minutes (24 hour clock)\n4️⃣ - month/day/year hour:minutes (24 hour clock)")
        embedmsg = await ctx.send(embed=em)
        await embedmsg.add_reaction("1️⃣")
        await embedmsg.add_reaction("2️⃣")
        await embedmsg.add_reaction("3️⃣")
        await embedmsg.add_reaction("4️⃣")

        def check(reaction, user):
            return embedmsg == reaction.message
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=60)
            except asyncio.TimeoutError:
                secondem = discord.Embed(title = "Timed out", description = "You took too long to react", color = discord.Color.orange())
                await embedmsg.edit(embed=secondem)
                await embedmsg.add_reaction("1️⃣")
                await embedmsg.add_reaction("2️⃣")
                await embedmsg.add_reaction("3️⃣")
                await embedmsg.add_reaction("4️⃣")
                break
            else:
                if str(reaction.emoji) == "1️⃣":
                    if user.name == self.bot.user.name:
                        continue
                    try:
                        writedateformat = {"data": {"dateformat": {"format":'%d/%m/%Y, %I:%M %p'}}}
                        with open(f"settings/dateformat-{ctx.guild.id}.json", 'w') as file:
                            json.dump(writedateformat, file)

                    except FileNotFoundError:
                        writedateformat = {"data": {"dateformat": {"format":'%d/%m/%Y, %I:%M %p'}}}
                        with open(f"settings/dateformat-{ctx.guild.id}.json", 'w') as file:
                            json.dump(writedateformat, file)

                    await embedmsg.clear_reaction("1️⃣")
                    await embedmsg.clear_reaction("2️⃣")
                    await embedmsg.clear_reaction("3️⃣")
                    await embedmsg.clear_reaction("4️⃣")

                    secondem = discord.Embed(title = "Date format set", description = "`day/month/year hour:minutes AM/PM` will now be used", color = discord.Color.green())
                    await embedmsg.edit(embed=secondem)
                    return

                if str(reaction.emoji) == "2️⃣":
                    if user.name == self.bot.user.name:
                        continue
                    try:
                        writedateformat = {"data": {"dateformat": {"format":'%m/%d/%Y, %I:%M %p'}}}
                        with open(f"settings/dateformat-{ctx.guild.id}.json", 'w') as file:
                            json.dump(writedateformat, file)
                        

                    except FileNotFoundError:
                        writedateformat = {"data": {"dateformat": {"format":'%m/%d/%Y, %I:%M %p'}}}
                        with open(f"settings/dateformat-{ctx.guild.id}.json", 'w') as file:
                            json.dump(writedateformat, file)
                
                    await embedmsg.clear_reaction("1️⃣")
                    await embedmsg.clear_reaction("2️⃣")
                    await embedmsg.clear_reaction("3️⃣")
                    await embedmsg.clear_reaction("4️⃣")

                    secondem = discord.Embed(title = "Date format set", description = "`month/day/year hour:minutes AM/PM` will now be used", color = discord.Color.green())
                    await embedmsg.edit(embed=secondem)
                    return

                if str(reaction.emoji) == "3️⃣":
                    if user.name == self.bot.user.name:
                        continue
                    try:
                        writedateformat = {"data": {"dateformat": {"format":'%d/%m/%Y, %H:%M'}}}
                        with open(f"settings/dateformat-{ctx.guild.id}.json", 'w') as file:
                            json.dump(writedateformat, file)

                    except FileNotFoundError:
                        writedateformat = {"data": {"dateformat": {"format":'%d/%m/%Y, %H:%M'}}}
                        with open(f"settings/dateformat-{ctx.guild.id}.json", 'w') as file:
                            json.dump(writedateformat, file)

                    await embedmsg.clear_reaction("1️⃣")
                    await embedmsg.clear_reaction("2️⃣")
                    await embedmsg.clear_reaction("3️⃣")
                    await embedmsg.clear_reaction("4️⃣")

                    secondem = discord.Embed(title = "Date format set", description = "`day/month/year hour:minutes (24 hour clock)` will now be used", color = discord.Color.green())
                    await embedmsg.edit(embed=secondem)
                    return

                if str(reaction.emoji) == "4️⃣":
                    if user.name == self.bot.user.name:
                        continue
                    try:
                        writedateformat = {"data": {"dateformat": {"format":'%m/%d/%Y, %H:%M'}}}
                        with open(f"settings/dateformat-{ctx.guild.id}.json", 'w') as file:
                            json.dump(writedateformat, file)

                    except FileNotFoundError:
                        writedateformat = {"data": {"dateformat": {"format":'%m/%d/%Y, %H:%M'}}}
                        with open(f"settings/dateformat-{ctx.guild.id}.json", 'w') as file:
                            json.dump(writedateformat, file)

                    await embedmsg.clear_reaction("1️⃣")
                    await embedmsg.clear_reaction("2️⃣")
                    await embedmsg.clear_reaction("3️⃣")
                    await embedmsg.clear_reaction("4️⃣")

                    secondem = discord.Embed(title = "Date format set", description = "`month/day/year hour:minutes (24 hour clock)` will now be used", color = discord.Color.green())
                    await embedmsg.edit(embed=secondem)
                    return

    @settings.command(name="filter")
    @commands.has_permissions(administrator=True)
    async def _filter(self, ctx, option):
        with open(f"settings/enablement-{ctx.guild.id}.json") as file:
            data = json.load(file)
        data = data["settings"]
        if str(option).lower() == "on":
            data["settings"]["filter"] = 1
            em = discord.Embed(title = 'The profanity filter is now turned on.', color = discord.Color.green())
        elif str(option).lower() == "off":
            data["settings"]["filter"] = 0
            em = discord.Embed(title = 'The profanity filter is now turned off.', color = discord.Color.green())
        #else:
        #    em = discord.Embed(title = "That argument isn't corrent.", color = discord.Color.red())
        #    await ctx.send(embed=em)
        #    return
        with open(f"settings/enablement-{ctx.guild.id}.json", 'w') as file:
            data = json.dump(data, file)
        await ctx.send(embed=em)

    @settings.command(name="disable")
    @commands.has_permissions(administrator=True)
    async def _disable (self, ctx, option):
        with open(f"settings/enablement-{ctx.guild.id}.json") as file:
            data = json.load(file)
        #data = data["settings"]
        if str(option).lower() == "true":
            data["settings"]["commands"] = 1
            #data.update({"commands": 1})
            em = discord.Embed(title = 'The profanity filter is now turned on.', color = discord.Color.green())
        elif str(option).lower() == "false":
            data["settings"]["commands"] = 0
            #data.update({"commands": 0})
            em = discord.Embed(title = 'The profanity filter is now turned off.', color = discord.Color.green())
        #else:
        #    em = discord.Embed(title = "That argument isn't corrent.", color = discord.Color.red())
        #    await ctx.send(embed=em)
        #    return
        with open(f"settings/enablement-{ctx.guild.id}.json", 'w') as file:
            data = json.dump(data, file)
        await ctx.send(embed=em)

def setup(bot):
    bot.add_cog(Settings(bot))
