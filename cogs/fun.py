import discord
from discord.ext import commands
import psutil
import config
import bot
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add(self, ctx, left: int, right: int):
        """Adds two numbers together."""
        em = discord.Embed(title = left + right)
        await ctx.send(embed = em)

    
    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        if "@everyone" in choices:
            em = discord.Embed(title = "Nice try, sadly that won't work here.")
            await ctx.send(embed = em)
        else:
            if "@here" in choices:
                em = discord.Embed(title = "Nice try, sadly that won't work here.")
                await ctx.send(embed = em)
            else:
                em = discord.Embed(title = random.choice(choices))
                await ctx.send(embed = em)
    
    @commands.command(description='#emotes')
    async def emote(self, ctx, emote: str):
        """emote command"""
        if str(emote) == "":
            emote = discord.utils.get.server.emojis()
        else:
            try:
                emote = discord.utils.get(self.bot.emojis, name=str(emote))
            except Exception as e:
                await ctx.send(str(e))
                return
        em = discord.Embed(title = "Here is the emote: ", body = emote)
        await ctx.send(embed = em)


    @commands.command()
    async def f(self, ctx, *, message2):
        em = discord.Embed(title = "F in the chat to: " + message2)
        msg = await ctx.send(embed = em)
        await msg.add_reaction('🇫')


        
def setup(bot):
    bot.add_cog(Fun(bot))
