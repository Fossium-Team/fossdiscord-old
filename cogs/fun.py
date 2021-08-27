# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.
import json
import os
import discord
# from discord import embeds
from discord.ext import commands
from discord_slash import cog_ext
# import psutil
# import config
# import bot
import random
from discord_slash import SlashContext
import wikipediaapi
import requests
import re


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.datapath = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__))), '..', 'cache')

    @commands.cooldown(1, 10, commands.BucketType.channel)
    #     @cog_ext.cog_slash(name='choose', description='Multiple choices.')
    @commands.command()
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        if "@everyone" in choices:
            em = discord.Embed(title="Nice try, sadly that won't work here.", color=discord.Color.red())
            await ctx.send(embed=em)
        else:
            if "@here" in choices:
                em = discord.Embed(title="Nice try, sadly that won't work here.", color=discord.Color.red())
                await ctx.send(embed=em)
            else:
                em = discord.Embed(title="The chosen word is:", description=random.choice(choices),
                                   color=discord.Color.blue())
                await ctx.send(embed=em)

    #    @commands.cooldown(1, 10, commands.BucketType.user)
    @cog_ext.cog_slash(name='cat', description='Get a cat picture.')
    #     @commands.command(aliases=['kat', 'cats', 'kitten'])
    async def cat(self, ctx):
        file = os.path.join(self.datapath, 'catpic.json')
        with open(file, 'r') as f:
            data = json.load(f)
        url = data[random.randint(0, 99)]['url']
        em = discord.Embed(title="Cat Picture:", color=discord.Color.blue())
        em.set_image(url=url)
        await ctx.send(embed=em)

    #    @commands.cooldown(1, 10, commands.BucketType.user)
    @cog_ext.cog_slash(name='dog', description='Get a dog picture.')
    #    @commands.command(aliases=['puppy', 'doggo'])
    async def dog(self, ctx):
        file = os.path.join(self.datapath, 'dogpic.json')
        with open(file, 'r') as f:
            data = json.load(f)
        url = data[random.randint(0, 99)]['url']
        em = discord.Embed(title="Dog Picture:", color=discord.Color.blue())
        em.set_image(url=url)
        await ctx.send(embed=em)

    #    @commands.cooldown(1, 10, commands.BucketType.user)
    @cog_ext.cog_slash(name='wiki', description='Search from wikipedia.')
    #     @commands.command(aliases=['wiki'])
    # async def wikipedia(self, ctx, *page):
    async def wikipedia(self, ctx, *, page):
        # if not page:
        #    em = discord.Embed(title='The argument `page` is missing', color=discord.Color.red())
        #    await ctx.send(embed=em)
        #    return
        # f len(page) >= 2:
        #    args = "_".join(page[:])
        # else:
        #    args = " ".join(page[:])
        firstem = discord.Embed(title="Getting data from Wikipedia...", color=discord.Color.orange())
        embedmsg = await ctx.send(embed=firstem)
        wiki_wiki = wikipediaapi.Wikipedia('en')
        page_py = wiki_wiki.page(page)
        if page_py.exists():
            if re.search("may refer to:", page_py.summary[0:500]):
                wiki_wiki = wikipediaapi.Wikipedia(
                    language='en',
                    extract_format=wikipediaapi.ExtractFormat.WIKI
                )
                url = f"https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search={args}&redirects=resolve"
                wiki_link = str(requests.get(url).json()[3]).replace("'", '').replace('[', '').replace(']', '').replace(
                    ",", " ")
                secondem = discord.Embed(title=f"{args} may refer to:", description=f"{wiki_link}...",
                                         color=discord.Color.blue())
                await embedmsg.edit(embed=secondem)
            else:
                secondem = discord.Embed(title=page_py.title, description=f"{page_py.summary[0:500]}...",
                                         color=discord.Color.blue())
                try:
                    imagejson = requests.get(
                        f"https://en.wikipedia.org/w/api.php?action=query&format=json&formatversion=2&prop=pageimages|pageterms&piprop=original&titles={args}").json()
                    imagelink = imagejson["query"]["pages"][0]["original"]["source"]
                    secondem.set_thumbnail(url=imagelink)
                except Exception:
                    pass
                secondem.set_footer(text=page_py.fullurl)
                await embedmsg.edit(embed=secondem)
        else:
            secondem = discord.Embed(title="That page doesn't exist", color=discord.Color.red())
            await embedmsg.edit(embed=secondem)


def setup(bot):
    bot.add_cog(Fun(bot))
