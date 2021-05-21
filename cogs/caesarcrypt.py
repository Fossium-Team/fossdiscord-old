import discord, time
from discord.ext import commands
import config

class Caesarcrypt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Twisted your message with caesarcrypt. @bot rounds(numbers) message")
    async def twisted_msg(self, ctx, rounds: int, *, message: str):
        """Encrypt a message."""
        await ctx.message.delete()
        if config.bot_lockdown_status == "no_lockdown":
            encrypt = ""
            message = str(message)
            for char in message:
                if not char.isalpha():
                    encrypt = encrypt + char
                elif char.isupper():
                    # for uppercase Z
                    encrypt = encrypt + chr((ord(char) + rounds - 65) % 26 + 65)
                else:
                    # for lowercase z
                    encrypt = encrypt + chr((ord(char) + rounds - 97) % 26 + 97)
            em = discord.Embed(title = 'Your encrypted message is: {}'.format(encrypt))
            await ctx.send(embed = em)
        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)


    @commands.command(description="Untwisted the message with caesarcrypt. @bot rounds(numbers) message")
    async def untwisted_msg(self, ctx, rounds: int, *, message: str):
        """Decrypt a message."""
        await ctx.message.delete()
        if config.bot_lockdown_status == "no_lockdown":
            decrypt = ""
            message = str(message)
            for char in message:
                if not char.isalpha():
                    decrypt = decrypt + char
                elif char.isupper():
                    # for uppercase Z
                    decrypt = decrypt + chr((ord(char) - rounds - 65) % 26 + 65)
                else:
                    # for lowercase z
                    decrypt = decrypt + chr((ord(char) - rounds - 97) % 26 + 97)

            em = discord.Embed(title = 'Your decrypted message is: {}'.format(decrypt))
            await ctx.send(embed = em)

        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(Caesarcrypt(bot))


# if config.bot_lockdown_status == "no_lockdown":
#    ...
# elif config.bot_lockdown_status == "lockdown_activated":
#    em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
#    await ctx.send(embed = em)
