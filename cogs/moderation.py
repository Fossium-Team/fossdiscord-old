# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import time
import os
import random
import asyncio
import config
import string
import json
from datetime import datetime

def timeconvertion(time):# Time convertion
    convertion = {"s": 1, "m": 60, "h": 3600, "d": 86400}
    letters_inside = ''.join(filter(str.isalpha, time))
    lettercount = len(letters_inside)
    to_convert = ''.join(filter(str.isdigit, time))
    if time[-1].isalpha() is True and time[0].isdigit() and lettercount == 1 and letters_inside in convertion and time.isalnum() == True:
            timeconverted = int(to_convert) * convertion[time[-1]]
            return int(timeconverted)
    return False

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount = None):
        if amount is None:
            em = discord.Embed(title = 'Usages:', color = discord.Color.blue())
            em.add_field(name = f"{config.prefix}purge <number of messages to purge>", value="Purge certain amount of messages.")
            em.add_field(name = f"{config.prefix}purge <mention> <how many messages to look back for message sent by user>", value="Purge certain amount of messages sent by a certain user.")
            await ctx.send(embed=em)
        else:
            await ctx.channel.purge(limit=int(amount)+1)

        if not os.path.exists('settings'):
            os.makedirs('settings')
        if os.path.isfile(f"settings/logging-{ctx.guild.id}.json"):
            with open(f"settings/logging-{ctx.guild.id}.json") as file:
                loggingjson = json.load(file)
            loggingchannel = loggingjson["data"]["logging"]["channel"]
            channel = self.bot.get_channel(int(loggingchannel))
            em = discord.Embed(title = f"{ctx.author} has purged {amount} messages in {ctx.message.channel}", color = discord.Color.orange())
            em.set_author(name=user, icon_url=user.avatar_url)
            em.add_field(name = "Reason", value = args)
            em.add_field(name = "Channel", value = ctx.message.channel)
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format
            datetimenow = datetime.now()
            currentdate = datetime.strftime(datetimenow, date_format)
            em.set_footer(text = f"{ctx.author}, at {currentdate}", icon_url = ctx.author.avatar_url)
            await channel.send(embed=em) 
        else:
            return
    
    @purge.command(name="user")
    @commands.has_permissions(manage_messages=True)
    async def _user(self, ctx, user: discord.Member = None, amount=10):
        if user is None:
            em = discord.Embed(title = 'The argument `user` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        await ctx.message.delete()
        await ctx.channel.purge(limit=int(amount), check=lambda message: message.author == user)

        if not os.path.exists('settings'):
            os.makedirs('settings')
        if os.path.isfile(f"settings/logging-{ctx.guild.id}.json"):
            with open(f"settings/logging-{ctx.guild.id}.json") as file:
                loggingjson = json.load(file)
            loggingchannel = loggingjson["data"]["logging"]["channel"]
            channel = self.bot.get_channel(int(loggingchannel))
            em = discord.Embed(title = f"{user} has purged all messages of {user} in the last {amount} messages", color = discord.Color.orange())
            em.set_author(name=user, icon_url=user.avatar_url)
            em.add_field(name = "Reason", value = args)
            em.add_field(name = "Channel", value = ctx.message.channel)
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format
            datetimenow = datetime.now()
            currentdate = datetime.strftime(datetimenow, date_format)
            em.set_footer(text = f"{ctx.author}, at {currentdate}", icon_url = ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            return

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member = None, *reason):
        """Kick a member."""
        if user is None:
            em = discord.Embed(title = 'The argument `user` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        args = " ".join(reason[:])
        if user == ctx.author:
            em = discord.Embed(title = "You cannot kick yourself", color = discord.Color.red())
        if not reason:
            await user.kick(reason=args)
            em = discord.Embed(title = f"**{user}** has been kicked.", color = discord.Color.orange())
            em.set_author(name = user, icon_url=user.avatar.url)
            em.add_field(name = "Reason", value = "none")
            await ctx.send(embed = em)
        else:
            await user.kick(reason=args)
            em = discord.Embed(title = f"**{user}** has been kicked.", color = discord.Color.orange())
            em.set_author(name = user, icon_url=user.avatar.url)
            em.add_field(name = "Reason", value = args)
            await ctx.send(embed = em)

        if not os.path.exists('settings'):
            os.makedirs('settings')
        if os.path.isfile(f"settings/logging-{ctx.guild.id}.json"):
            with open(f"settings/logging-{ctx.guild.id}.json") as file:
                loggingjson = json.load(file)
            loggingchannel = loggingjson["data"]["logging"]["channel"]
            channel = self.bot.get_channel(int(loggingchannel))
            em = discord.Embed(title = f"{user} has been kicked", color = discord.Color.orange())
            em.set_author(name=user, icon_url=user.avatar_url)
            em.add_field(name = "Reason", value = args)
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format
            datetimenow = datetime.now()
            currentdate = datetime.strftime(datetimenow, date_format)
            em.set_footer(text = f"{ctx.author}, at {currentdate}", icon_url = ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member = None, *reason):
        """Ban a member."""
        if user is None:
            em = discord.Embed(title = 'The argument `user` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        args = " ".join(reason[:])
        if user == ctx.author:
            em = discord.Embed(title = "You cannot ban yourself", color = discord.Color.red())
        if not reason:
            await user.ban(reason=args)
            em = discord.Embed(title = f"**{user}** has been banned", color = discord.Color.red())
            em.set_author(name = user, icon_url=user.avatar.url)
            em.add_field(name = "Reason", value = "none")
            await ctx.send(embed = em)
        else:
            await user.ban(reason=args)
            em = discord.Embed(title = f"**{user}** has been banned", color = discord.Color.red())
            em.set_author(name = user, icon_url=user.avatar.url)
            em.add_field(name = "Reason", value = "none")
            await ctx.send(embed = em)

        if not os.path.exists('settings'):
            os.makedirs('settings')
        if os.path.isfile(f"settings/logging-{ctx.guild.id}.json"):
            with open(f"settings/logging-{ctx.guild.id}.json") as file:
                loggingjson = json.load(file)
            loggingchannel = loggingjson["data"]["logging"]["channel"]
            channel = self.bot.get_channel(int(loggingchannel))
            em = discord.Embed(title = f"{user} has been banned", color = discord.Color.red())
            em.set_author(name=user, icon_url=user.avatar_url)
            em.add_field(name = "Reason", value = args)
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format
            datetimenow = datetime.now()
            currentdate = datetime.strftime(datetimenow, date_format)
            em.set_footer(text = f"{ctx.author}, at {currentdate}", icon_url = ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            return


    @commands.command() # Takes 1s 1m 1h 1d
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, user: discord.Member = None, mutetime = None):
        #BTW need to import time&asyncio module to work.
        """Mute a member."""
        if user is None:
            em = discord.Embed(title = 'The argument `user` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        if mutetime is None:
            em = discord.Embed(title = 'The argument `mutetime` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        if get(ctx.guild.roles, name="Muted"):
            pass
        else:
            #permission = discord.Permissions(send_messages=False, read_messages=False)
            #await ctx.guild.create_role(name="Muted", colour=discord.Colour(000000), permissions = permission)
            guildowner = ctx.bot.get_user(int(ctx.guild.owner_id))
            em = discord.Embed(title = "A role named `Muted` does not exist in your server, please create it first. And also make sure to create overrides for the channels you don't want a muted user speaking in.", color = discord.Color.red())
            await guildowner.send(embed = em)
            return
        if timeconvertion(mutetime) is not False:
            role = discord.utils.get(user.guild.roles, name="Muted")
            if role in user.roles:
                em = discord.Embed(title = f"`{user.display_name}` is already muted", color = discord.Color.red())
                await ctx.send(embed = em)
                return
            else:
                await user.add_roles(role)
            em = discord.Embed(title = f"`{user.display_name}` has been muted for " + "`{}`".format(str(mutetime)), color = discord.Color.orange())
            await ctx.send(embed = em)
            await asyncio.sleep(timeconvertion(mutetime))
            await user.remove_roles(role)
        elif timeconvertion(mutetime) is False:
            em = discord.Embed(title = "The time format doesn't seem right", color = discord.Color.red())
            await ctx.send(embed = em)

        if not os.path.exists('settings'):
            os.makedirs('settings')
        if os.path.isfile(f"settings/logging-{ctx.guild.id}.json"):
            with open(f"settings/logging-{ctx.guild.id}.json") as file:
                loggingjson = json.load(file)
            loggingchannel = loggingjson["data"]["logging"]["channel"]
            channel = self.bot.get_channel(int(loggingchannel))
            em = discord.Embed(title = f"{user} has been muted", color = discord.Color.orange())
            em.set_author(name=user, icon_url=user.avatar_url)
            em.add_field(name = "Mute time", value = str(mutetime))
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format
            datetimenow = datetime.now()
            currentdate = datetime.strftime(datetimenow, date_format)
            em.set_footer(text = f"{ctx.author}, at {currentdate}", icon_url = ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            return
            
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: discord.Member = None):
        """Unmute a member."""
        if user is None:
            em = discord.Embed(title = 'The argument `user` is red', color = discord.Color.orange())
            await ctx.send(embed = em)
            return
        role = discord.utils.get(user.guild.roles, name="Muted")
        if role not in user.roles:
            em = discord.Embed(title = f"`{user.display_name}` is not muted", color = discord.Color.red())
            await ctx.send(embed = em)
            return
        else:
            await user.remove_roles(role)
        em = discord.Embed(title = f"Unmuted `{user.display_name}`", color = discord.Color.green())
        await ctx.send(embed = em)

        if not os.path.exists('settings'):
            os.makedirs('settings')
        if os.path.isfile(f"settings/logging-{ctx.guild.id}.json"):
            with open(f"settings/logging-{ctx.guild.id}.json") as file:
                loggingjson = json.load(file)
            loggingchannel = loggingjson["data"]["logging"]["channel"]
            channel = self.bot.get_channel(int(loggingchannel))
            em = discord.Embed(title = f"{user} has been unmuted", color = discord.Color.orange())
            em.set_author(name=user, icon_url=user.avatar_url)
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format
            datetimenow = datetime.now()
            currentdate = datetime.strftime(datetimenow, date_format)
            em.set_footer(text = f"{ctx.author}, at {currentdate}", icon_url = ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def softban(self, ctx, user: discord.Member = None, *reason):
        if user is None:
            em = discord.Embed(title = 'The argument `user` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        args = " ".join(reason[:])
        if user == ctx.author:
            em = discord.Embed(title = "You cannot softban yourself", color = discord.Color.red())
        if not reason:
            await ctx.guild.ban(user)
            await ctx.guild.unban(user)
            em = discord.Embed(title = f"**{user}** has been banned", color = discord.Color.red())
            em.set_author(name = user, icon_url=user.avatar.url)
            em.add_field(name = "Reason", value = "none")
            await ctx.send(embed = em)
        else:
            await ctx.guild.ban(user)
            await ctx.guild.unban(user)
            em = discord.Embed(title = f"**{user}** has been banned", color = discord.Color.red())
            em.set_author(name = user, icon_url=user.avatar.url)
            em.add_field(name = "Reason", value = "none")
            await ctx.send(embed = em)

        if not os.path.exists('settings'):
            os.makedirs('settings')
        if os.path.isfile(f"settings/logging-{ctx.guild.id}.json"):
            with open(f"settings/logging-{ctx.guild.id}.json") as file:
                loggingjson = json.load(file)
            loggingchannel = loggingjson["data"]["logging"]["channel"]
            channel = self.bot.get_channel(int(loggingchannel))
            em = discord.Embed(title = f"{user} has been softbanned", color = discord.Color.orange())
            em.set_author(name=user, icon_url=user.avatar_url)
            em.add_field(name = "Reason", value = args)
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format
            datetimenow = datetime.now()
            currentdate = datetime.strftime(datetimenow, date_format)
            em.set_footer(text = f"{ctx.author}, at {currentdate}", icon_url = ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            return

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.Member = None):
        if not user:
            em = discord.Embed(title = 'The argument `user` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        await ctx.guild.unban(user)
        em = discord.Embed(title = f"**{user}** has been unbanned", color = discord.Color.green())
        await ctx.send(embed = em)

        if not os.path.exists('settings'):
            os.makedirs('settings')
        if os.path.isfile(f"settings/logging-{ctx.guild.id}.json"):
            with open(f"settings/logging-{ctx.guild.id}.json") as file:
                loggingjson = json.load(file)
            loggingchannel = loggingjson["data"]["logging"]["channel"]
            channel = self.bot.get_channel(int(loggingchannel))
            em = discord.Embed(title = f"{user} has been unbanned", color = discord.Color.orange())
            em.set_author(name=user, icon_url=user.avatar_url)
            em.add_field(name = "Reason", value = args)
            if os.path.isfile(f"settings/dateformat-{ctx.guild.id}.json"):
                with open(f"settings/dateformat-{ctx.guild.id}.json") as file:
                    dateformatjson = json.load(file)
                date_format = dateformatjson["data"]["dateformat"]["format"]
            else:
                date_format = config.date_format
            datetimenow = datetime.now()
            currentdate = datetime.strftime(datetimenow, date_format)
            em.set_footer(text = f"{ctx.author}, at {currentdate}", icon_url = ctx.author.avatar_url)
            await channel.send(embed=em)
        else:
            return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, user : discord.Member = None, *, reason = "no reason provided"):
        if user is None:
            em = discord.Embed(title = 'The argument `user` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        userid = user.id
        if not os.path.exists('warnings'):
            os.makedirs('warnings')
        try:
            with open(f"warnings/warnings-{ctx.guild.id}.json", "r") as file:
                data = json.load(file)
        except Exception:
            data = {"data":{f"{userid}":{"userid":f"{userid}","count": 1,"case":{"1": f"{reason}"}}}}
            with open(f"warnings/warnings-{ctx.guild.id}.json", "w") as file:
                json.dump(data, file, indent=4)
            em = discord.Embed(title = "Successfully warned that member", color = discord.Color.orange())
            await ctx.send(embed=em)
            return
        try:
            data["data"]
        except (IndexError, KeyError):
            data = {"data":{f"{userid}":{"userid":f"{userid}","count": 1,"case":{"1": f"{reason}"}}}}
            with open(f"warnings/warnings-{ctx.guild.id}.json", "w") as file:
                json.dump(data, file, indent=4)
            em = discord.Embed(title = "Successfully warned that member", color = discord.Color.orange())
            await ctx.send(embed=em)
            return
        try:
            for attr, value in data["data"][f"{user.id}"]["case"].items():
                count = attr
            caseid = int(count) + 1
            data["data"][f"{userid}"]["case"].update({f"{caseid}": f"{reason}"})
            data["data"][f"{userid}"]["count"] = len(data["data"][f"{userid}"]["case"])
            with open(f"warnings/warnings-{ctx.guild.id}.json", "w") as file:
                json.dump(data, file, indent=4)
        except Exception:
            data = {"data":{f"{userid}":{"userid":f"{userid}","count": 1,"case":{"1": f"{reason}"}}}}
            with open(f"warnings/warnings-{ctx.guild.id}.json", "w") as file:
                json.dump(data, file, indent=4)
        em = discord.Embed(title = "Successfully warned that member", color = discord.Color.orange())
        await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, user : discord.Member = None):
        if user is None:
            em = discord.Embed(title = 'The argument `user` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        userid = user.id
        if not os.path.isdir("warnings"):
            os.makedirs("warnings")
            em = discord.Embed(title = "Nobody has been warned yet", color = discord.Color.green())
            await ctx.send(embed = em)
            return
        elif not os.path.isfile(f"warnings/warnings-{ctx.guild.id}.json"):
            em = discord.Embed(title = "Nobody in this guild has been warned yet", color = discord.Color.green())
            await ctx.send(embed = em)
            return
        elif os.stat(f"warnings/warnings-{ctx.guild.id}.json").st_size == 0:
            em = discord.Embed(title = "Nobody in this guild has been warned yet", color = discord.Color.green())
            await ctx.send(embed = em)
            return
        with open(f"warnings/warnings-{ctx.guild.id}.json") as file:
            data = json.load(file)
        try:
            user_warns = data["data"][f"{userid}"]
        except (IndexError, KeyError):
            em = discord.Embed(title = f"`{user.display_name}` doesn't have any warnings", color = discord.Color.green())
            await ctx.send(embed = em)
            return
        case_count = data["data"][f"{userid}"]["count"]
        if case_count == 0:
            em = discord.Embed(title = f"`{user.display_name}` doesn't have any warnings", color = discord.Color.green())
            await ctx.send(embed = em)
            return
        em = discord.Embed(title = f"`{user.display_name}`'s warnings:", color = discord.Color.blue())
        for attr, value in data["data"][f"{user.id}"]["case"].items():
            em.add_field(name = f"Case number #{attr}:", value = f"{value}")
        await ctx.send(embed = em)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def delwarning(self, ctx, user : discord.Member = None, casenumber = None):
        if user is None:
            em = discord.Embed(title = 'The argument `user` is missing', color = discord.Color.red())
            await ctx.send(embed = em)
            return
        userid = user.id
        if not os.path.isdir("warnings"):
            os.makedirs("warnings")
            em = discord.Embed(title = "Nobody has been warned yet", color = discord.Color.green())
            await ctx.send(embed = em)
            return
        elif not os.path.isfile(f"warnings/warnings-{ctx.guild.id}.json"):
            em = discord.Embed(title = "Nobody in this guild has been warned yet", color = discord.Color.green())
            await ctx.send(embed = em)
            return
        elif os.stat(f"warnings/warnings-{ctx.guild.id}.json").st_size == 0:
            em = discord.Embed(title = "Nobody in this guild has been warned yet", color = discord.Color.green())
            await ctx.send(embed = em)
            return
        elif casenumber is None:
            #em = discord.Embed(title = 'The argument `casenumber` is missing', color = discord.Color.red())
            #await ctx.send(embed = em)
            #return
            try:
                with open(f"warnings/warnings-{ctx.guild.id}.json") as file:
                    data = json.load(file)
                cases = []
                for attr, value in data["data"][f"{userid}"]["case"].items():
                    cases.append(attr)
                for case in cases:
                    del data["data"][f"{userid}"]["case"][str(case)]
                data["data"][f"{userid}"]["count"] = len(data["data"][f"{userid}"]["case"])
                with open(f"warnings/warnings-{ctx.guild.id}.json", "w") as file:
                    json.dump(data, file, indent=4)
                em = discord.Embed(title = f"Successfully cleared all the warnings of {user.display_name}", color = discord.Color.green())
                await ctx.send(embed = em)
            except (IndexError, KeyError):
                em = discord.Embed(title = "The warning you are trying to remove does not exist", color = discord.Color.red())
                await ctx.send(embed = em)
                return
        else:
            if casenumber[0] != "#" or not casenumber[1:].isalnum():
                em = discord.Embed(title = "Your `casenumber` format is not right", color = discord.Color.red())
                await ctx.send(embed = em)
                return
            else:
                if casenumber[0] == "#":
                    casenumber = casenumber[1:]
            try:
                with open(f"warnings/warnings-{ctx.guild.id}.json") as file:
                    data = json.load(file)
                del data["data"][f"{userid}"]["case"][casenumber]
                data["data"][f"{userid}"]["count"] = len(data["data"][f"{userid}"]["case"])
                with open(f"warnings/warnings-{ctx.guild.id}.json", "w") as file:
                    json.dump(data, file, indent=4)
            except (IndexError, KeyError):
                em = discord.Embed(title = "The warning you are trying to remove does not exist", color = discord.Color.red())
                await ctx.send(embed = em)
                return
            em = discord.Embed(title = "Successfully removed that warning", delete_after=10.0, color = discord.Color.green())
            await ctx.send(embed=em)

    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_nicknames=True)
    async def modnick(self, ctx, *, user: discord.Member = None):
        if user is None:
            em = discord.Embed(title = 'Usage:', color = discord.Color.blue())
            em.add_field(name = f"{config.prefix}modnick <user ID or mention>", value='Moderates the nickname of a user or a bot (sets the nickname to "ModdedNick-(random letters and numbers)"')
            await ctx.send(embed=em)
        else:
            source = string.ascii_letters + string.digits
            result_str = ''.join((random.choice(source) for i in range(8)))
            newnickname = f"ModdedNick-{result_str}"
            await user.edit(nick=newnickname)
            await ctx.message.delete()
            em = discord.Embed(title = f'Nickname was moderated.', color = discord.Color.orange())
            em.add_field(name=f"{user.name}#{user.discriminator}", value=user.mention)
            await ctx.send(embed=em, delete_after=10.0)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_nicknames=True)
    async def changenick(self, ctx, user: discord.Member = None, *nick):
        args = " ".join(nick[:])
        if user is None:
            em = discord.Embed(title = 'Usage:', color = discord.Color.blue())
            em.add_field(name = f"{config.prefix}changenick <user ID or mention> <new nickname (if not given the nickname will be reset)>", value="Changes the nickname of a user or a bot.")
            await ctx.send(embed=em)
        await user.edit(nick=args)
        await ctx.message.delete()
        em = discord.Embed(title = f'Nickname was changed.', color = discord.Color.orange())
        em.add_field(name=f"{user.name}#{user.discriminator}", value=user.mention)
        await ctx.send(embed=em, delete_after=10.0)

def setup(bot):
    bot.add_cog(Moderation(bot))