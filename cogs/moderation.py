# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord
import time, os, random, asyncio, config, string
from discord.ext import commands
from discord.utils import get

def timeconvertion(time):# Time convertion
    convertion = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    letters_inside = ''.join(filter(str.isalpha, time))
    lettercount = len(letters_inside)
    to_convert = ''.join(filter(str.isdigit, time))
    if time[-1].isalpha() is True and time[0].isdigit() and lettercount == 1 and letters_inside in convertion and time.isalnum() == True:
        timeconverted = int(to_convert) * convertion[time[-1]]
        return int(timeconverted)
    else:
        return False

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=10):
        """Purge messages, default amount is 10."""
        await ctx.channel.purge(limit=amount+1)
    
    @purge.command(name="user")
    async def _user(self, ctx, user: discord.Member, amount=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount, check=lambda message: message.author == user)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *reason):
        """Kick a member."""
        args = " ".join(reason[:])
        if not reason:
            await user.kick()
            em = discord.Embed(title = f"**{user}** has been kicked, reason: **none**.", color = discord.Color.orange())
            await ctx.send(embed = em)
        else:
            await user.kick()
            em = discord.Embed(title = f"**{user}** has been kicked, reason: **{args}**.", color = discord.Color.orange())
            await ctx.send(embed = em)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *reason):
        """Ban a member."""
        args = " ".join(reason[:])
        if not reason:
            await user.ban()
            em = discord.Embed(title = f"**{user}** has been banned, reason: **none**.", color = discord.Color.red())
            await ctx.send(embed = em)
        else:
            await user.ban()
            em = discord.Embed(title = f"**{user}** has been banned, reason: **{args}**.", color = discord.Color.red())
            await ctx.send(embed = em)


    @commands.command() # Takes 1s 1m 1h 1d
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member, mutetime):
        #BTW need to import time&asyncio module to work.
        """Mute a member."""
        if get(ctx.guild.roles, name="Muted"):
            pass
        else:
            #permission = discord.Permissions(send_messages=False, read_messages=False)
            #await ctx.guild.create_role(name="Muted", colour=discord.Colour(000000), permissions = permission)
            guildowner = ctx.bot.get_user(int(ctx.guild.owner_id))
            em = discord.Embed(title = "A role named 'Muted' does not exist in your server, please create it first. And also make sure to create overrides for the channels you don't want a muted user speaking in.", color = discord.Color.red())
            await guildowner.send(embed = em)
            return
        if timeconvertion(mutetime) is False:
            try:
                role = discord.utils.get(user.guild.roles, name="Muted")
                await user.add_roles(role)
            except Exception:
                em = discord.Embed(title = "User already muted, mute him again is not necessary.", color = discord.Color.red())
                await ctx.send(embed = em)
                return
            em = discord.Embed(title = "User has been muted for " + "`{}`".format(str(mutetime)) + ".", color = discord.Color.orange())
            await ctx.send(embed = em)
            await asyncio.sleep(timeconvertion(mutetime))
            await user.remove_roles(role)
        elif timeconvertion(mutetime) == False:
            em = discord.Embed(title = "The time format doesn't seem right.", color = discord.Color.red())
            await ctx.send(embed = em)


    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.Member, *reason):
        args = " ".join(reason[:])
        await ctx.guild.ban(user)
        await ctx.guild.unban(user)
        if not reason:
            em = discord.Embed(title = f"**{user}** has been softbanned, reason: **none**.", color = discord.Color.orange())
            await ctx.send(embed = em)
        else:
            em = discord.Embed(title = f"**{user}** has been softbanned, reason: **{args}**.", color = discord.Color.orange())
            await ctx.send(embed = em)


    '''@commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        """Unban a member."""
        userToUnban = await self.bot.fetch_user(id)
        await ctx.guild.unban(userToUnban)
        em = discord.Embed(title = "Successfully unbanned `" + userToUnban.name + "`.", color = discord.Color.green())
        await ctx.send(embed = em)'''

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.Member):
        await ctx.guild.unban(user)
        em = discord.Embed(title = f"**{user}** has been unbanned", color = discord.Color.green())

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member):
        """Unmute a member."""
        role = discord.utils.get(user.guild.roles, name="Muted")
        await user.remove_roles(role)
        em = discord.Embed(title = "Successfully unmuted `" + user.name + "`", color = discord.Color.green())
        await ctx.send(embed = em)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, user : discord.Member, *reason):
        args = " ".join(reason[:])

        if not os.path.exists('warns'):
            os.makedirs('warns')
        try:
            if os.stat(f"warns/{str(user.id)}_{str(ctx.message.guild.id)}.py").st_size > 0:
                em = discord.Embed(title = "Successfully warned that member.", color = discord.Color.orange())
                await ctx.send(embed=em)
                writeReasonTemplate = str(args)
                warns = open(f"warns/{str(user.id)}_{str(ctx.message.guild.id)}.py", 'a')
                warns.write("\n")
                warns.write(writeReasonTemplate)
                warns.close()

            elif os.stat(f"warns/{str(user.id)}_{str(ctx.message.guild.id)}.py").st_size == 0:
                em = discord.Embed(title = "Successfully warned that member.", color = discord.Color.orange())
                await ctx.send(embed=em)
                writeReasonTemplate = str(args)
                warns = open(f"warns/{str(user.id)}_{str(ctx.message.guild.id)}.py", 'a')
                warns.write(writeReasonTemplate)
                warns.close()
        except:
            em = discord.Embed(title = "Successfully warned that member.", color = discord.Color.orange())
            await ctx.send(embed=em)
            writeReasonTemplate = str(args)
            warns = open(f"warns/{str(user.id)}_{str(ctx.message.guild.id)}.py", 'a')
            warns.write(writeReasonTemplate)
            warns.close()


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warns(self, ctx, user : discord.Member):
        if not os.path.exists('warns'):
            os.makedirs('warns')
        try:
            if os.stat("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py").st_size > 0:
                with open("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py") as f:
                    lines = f.readlines()
                    lines_clean = "".join(lines[:])
                    if not lines_clean:
                        em = discord.Embed(title = "Warns for " + str(user), description = "This user has no warnings", color = discord.Color.orange())
                    else:
                        em = discord.Embed(title = "Warns for " + str(user), description = lines_clean, color = discord.Color.orange())
                        await ctx.send(embed = em)
            elif os.stat("warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py").st_size == 0:
                em = discord.Embed(title = "Warns for " + str(user), description = "This user has no warnings", color = discord.Color.orange())
                await ctx.send(embed = em)
        except:
            em = discord.Embed(title = "Warns for " + str(user), description = "This user has no warnings", color = discord.Color.orange())
            await ctx.send(embed = em)


    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx, user : discord.Member, *, reason):
        if not os.path.exists('warns'):
            os.makedirs('warns')
        fn = "warns/" + str(user.id) + "_" + str(ctx.message.guild.id) + ".py"
        f = open(fn)
        output = []
        word=str(reason)
        for line in f:
            if not line.startswith(word):
                output.append(line)
        f.close()
        f = open(fn, 'w')
        f.writelines(output)
        f.close()
        em = discord.Embed(title = "Successfully removed that warning.", delete_after=10.0, color = discord.Color.green())
        await ctx.send(embed=em)

    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_nicknames=True)
    async def modnick(self, ctx, *, user: discord.Member):
        source = string.ascii_letters + string.digits
        result_str = ''.join((random.choice(source) for i in range(8)))
        newnickname = f"ModdedNick{result_str}"
        await user.edit(nick=newnickname)
        await ctx.message.delete()
        await ctx.send(f'Nickname was moderated for {user.mention} ({user.name}#{user.discriminator}).', delete_after=10.0, color = discord.Color.orange())


    @commands.command(pass_context=True)
    @commands.has_permissions(manage_nicknames=True)
    async def changenick(self, ctx, user: discord.Member, nick):
        await user.edit(nick=nick)
        await ctx.message.delete()
        await ctx.send(f'Nickname was changed for {user.mention} ({user.name}#{user.discriminator}).', delete_after=10.0, color = discord.Color.orange())

def setup(bot):
    bot.add_cog(Moderation(bot))
