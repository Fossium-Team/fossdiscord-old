# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord
from discord import embeds
from discord.ext import commands
import psutil
import config
import bot
import random
import wikipediaapi
import requests
import re
from flickrapi import FlickrAPI

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.cooldown(1, 15, commands.BucketType.channel)
    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        if "@everyone" in choices:
            em = discord.Embed(title = "Nice try, sadly that won't work here.", color = discord.Color.red())
            await ctx.send(embed = em)
        else:
            if "@here" in choices:
                em = discord.Embed(title = "Nice try, sadly that won't work here.", color = discord.Color.red())
                await ctx.send(embed = em)
            else:
                em = discord.Embed(title = random.choice(choices), color = discord.Color.orange())
                await ctx.send(embed = em)

    @commands.cooldown(1, 15, commands.BucketType.channel)
    @commands.command()
    async def f(self, ctx, *, message2):
        em = discord.Embed(title = f"F in the chat to: **{message2}**", color=discord.Color.green())
        msg = await ctx.send(embed = em)
        await msg.add_reaction('🇫')

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['kat','cats', 'kitten'])
    async def cat(self, ctx):
        firstem = discord.Embed(title = "Getting cat picture...", color = discord.Color.orange())
        embedmsg = await ctx.send(embed=firstem)
        request = requests.get("https://api.thecatapi.com/v1/images/search?format=json").json()
        url = request[0]["url"]
        secondem = discord.Embed(title = "Cat Picture:", color = discord.Color.blue())
        secondem.set_image(url=url)
        await embedmsg.edit(embed=secondem)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['puppy','doggo'])
    async def dog(self, ctx):
        firstem = discord.Embed(title = "Getting dog picture...", color = discord.Color.orange())
        embedmsg = await ctx.send(embed=firstem)
        request = requests.get("https://api.thedogapi.com/v1/images/search").json()
        url = request[0]["url"]
        secondem = discord.Embed(title = "Dog Picture:", color = discord.Color.blue())
        secondem.set_image(url=url)
        await embedmsg.edit(embed=secondem)

    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.command(aliases=['wiki'])
    async def wikipedia(self, ctx, *page):
        if len(page) >= 2:
            args = "_".join(page[:])
        else:
            args = " ".join(page[:])
        firstem = discord.Embed(title = "Getting data from Wikipedia...", color = discord.Color.orange())
        embedmsg = await ctx.send(embed=firstem)
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(args)
        if page_py.exists():
            if re.search("may refer to:", page_py.summary[0:500]):
                wiki_wiki = wikipediaapi.Wikipedia(
                        language='en',
                        extract_format=wikipediaapi.ExtractFormat.WIKI
                )
                url = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search={args}&redirects=resolve"
                wiki_link = str(requests.get(url).json()[3]).replace("'", '').replace('[', '').replace(']', '').replace(",", " ")
                secondem = discord.Embed(title = f"{args} may refer to:", description = f"{wiki_link}...", color = discord.Color.blue())
                await embedmsg.edit(embed=secondem)
            else:
                secondem = discord.Embed(title = page_py.title, description = f"{page_py.summary[0:500]}...", color = discord.Color.blue())
                try:
                    imagejson = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={args}").json()
                    imagelink = imagejson["query"]["pages"][0]["original"]["source"]
                    secondem.set_thumbnail(url=imagelink)
                except Exception:
                    pass
                secondem.set_footer(text=page_py.fullurl)
                await embedmsg.edit(embed=secondem)
        else:
            secondem = discord.Embed(title = "That page doesn't exist", color = discord.Color.red())
            await embedmsg.edit(embed=secondem)
def setup(bot):
    bot.add_cog(Fun(bot))
