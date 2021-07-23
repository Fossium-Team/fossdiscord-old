# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import config
import datetime
import time
import requests
import re
import json
import os
start_time = time.time()
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def ping(self, ctx):
        '''
        Get the latency of the bot.
        '''
        em = discord.Embed(title = "Pong! `"f"{round(self.bot.latency*1000)} ms`.", color = discord.Color.green())
        await ctx.send(embed = em)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Get a link to somebody's avatar."""
        if user is None:
            user = ctx.author
            em = discord.Embed(title = f"{user.name}'s avatar", color = discord.Color.blue())
            em.set_image(url=user.avatar_url)
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = f"{user.name}'s avatar", color = discord.Color.blue())
            em.set_image(url=user.avatar_url)
            await ctx.send(embed = em)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['whois'])
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """Gives information about a user."""
        if user is None:
            user = ctx.author
            if user.display_name == user.name:
                usernickname = "None"
            else:
                usernickname = user.display_name

            if not os.path.exists('settings'):
                os.makedirs('settings')
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format

            embed = discord.Embed(color = discord.Color.blue())
            embed.set_author(name=str(user), icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="ID", value=user.id)
            embed.add_field(name="Nickname", value=usernickname)
            embed.add_field(name="Joined Server", value=user.joined_at.strftime(date_format), inline=False)
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            embed.add_field(name="Registered", value=user.created_at.strftime(date_format), inline=True)
            perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
            embed.add_field(name="Guild permissions", value=perm_string, inline=False)
            return await ctx.send(embed=embed)
        else:
            if user.display_name == user.name:
                usernickname = "None"
            else:
                usernickname = user.display_name

            if not os.path.exists('settings'):
                os.makedirs('settings')
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format

            embed = discord.Embed(color = discord.Color.blue())
            embed.set_author(name=str(user), icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.add_field(name="ID", value=user.id)
            embed.add_field(name="Nickname", value=usernickname)
            embed.add_field(name="Joined", value=user.joined_at.strftime(date_format), inline=False)
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            embed.add_field(name="Registered", value=user.created_at.strftime(date_format), inline=True)
            perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
            embed.add_field(name="Guild permissions", value=perm_string, inline=False)
            return await ctx.send(embed=embed)
        if isinstance(ctx.channel, discord.DMChannel):
            return

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def joined(self, ctx, *member: discord.Member):
        """Says when a member joined."""
        if not member:
            em = discord.Embed(title = 'The argument `member` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        em = discord.Embed(title = '{0.name} joined in {0.joined_at}'.format(member), color = discord.Color.blue())
        await ctx.send(embed = em)


    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def serverinfo(self, ctx):
        """Gives some information about the server."""
        role_count = len(ctx.guild.roles)
        name = str(ctx.guild.name)
        description = "Description: " + str(ctx.guild.description)
        owner = str(ctx.guild.owner)
        id = str(ctx.guild.id)
        region = str(ctx.guild.region)
        memberCount = str(ctx.guild.member_count)
        icon = str(ctx.guild.icon_url)
        embed = discord.Embed(
            description=description,
            color=discord.Color.blue()
            )

        if not os.path.exists('settings'):
            os.makedirs('settings')
        if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
            with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                dateformatjson = json.load(file)
            date_format = dateformatjson["data"]["dateformat"]["format"]
        else:
            date_format = config.date_format
            
        embed.set_thumbnail(url=icon)
        embed.set_author(name=name, icon_url=icon)
        embed.add_field(name="Owner", value=owner, inline=True)
        embed.add_field(name="Server ID", value=id, inline=True)
        embed.add_field(name="Server Created", value=ctx.guild.created_at.__format__(date_format))
        embed.add_field(name="Region", value=region, inline=True)
        embed.add_field(name="Number of Members", value=memberCount, inline=True)
        embed.add_field(name="Number of Roles", value=str(role_count), inline=True)

        await ctx.send(embed=embed)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(description='#emotes')
    async def emote(self, ctx, emote : discord.Emoji = None):
        if emote == None:
            em = discord.Embed(title = 'The argument `emote` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        else:
            try:
                em = discord.Embed(timestamp=emote.created_at, color = discord.Color.green())
                em.set_author(name=emote.name, icon_url=emote.url)
                em.set_thumbnail(url=emote.url)
                em.set_footer(text="Created on")
                em.add_field(name="ID", value=emote.id)
                em.add_field(name="Usage", value=f"`{emote}`")
                em.add_field(name="URL", value=f"<{emote.url}>")
                await ctx.send(embed=em)
                return
            except Exception:
                em = discord.Embed(title="That emote probably is not in the server(s) that the bot is in.")
                await ctx.send(embed=em)
                return

        # else:
        #     try:
        #         emote = discord.utils(self.bot.get_all_emojis())
        #         emote = discord.utils.get(self.bot.Emoji, name=emote)
        #     except Exception as e:
        #         await ctx.send(str(e))
        #         return

    @commands.cooldown(1, 10, commands.BucketType.channel)
    @commands.command()
    async def quickpoll(self, ctx, *poll):
        if not poll:
            em = discord.Embed(title = 'The argument `poll` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        await ctx.message.delete()
        args = " ".join(poll[:])
        em = discord.Embed(title = f'{args}')
        msg = await ctx.send(embed = em)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
    
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(name="Uptime", value=text)
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + text)

# going to change this when the Down for Everyone or Just Me API is released
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command()
    async def isitdown(self, ctx, *website):
        if not website:
            em = discord.Embed(title = 'The argument `website` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        if re.search("https://", website):
            pass
        else:
            website = f"https://{website}"
        firstem = discord.Embed(title = f"Checking if {website} is down... This may take a few seconds...", color = discord.Color.orange())
        embedmsg = await ctx.send(embed = firstem)
        try:
            websiteresponse = requests.get(website)
        except Exception:
            secondem = discord.Embed(title = f"An error occured, it is most likely that {website} doesn't exist or it is down", color = discord.Color.red())
            await embedmsg.edit(embed=secondem)
            return
        if websiteresponse.ok:
            secondem = discord.Embed(title = f"{website} is online", color = discord.Color.green())
            await embedmsg.edit(embed=secondem)
        else:
            secondem = discord.Embed(title = f"{website} is down", color = discord.Color.red())
            await embedmsg.edit(embed=secondem)

def setup(bot):
    bot.add_cog(Utils(bot))
