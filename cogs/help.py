# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import config
import globalconfig
import requests
import asyncio


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(5, 15, commands.BucketType.channel)
    @commands.group(invoke_without_command=True, aliases=['commands'])
    async def help(self, ctx):
        em = discord.Embed(title = "Help", color = discord.Color.red())
        em.add_field(name = "Options", value = "🏠 - Home (this page)\n⚔️ - Moderation\n⚙️ - Settings\n🪛 - Utils\n😄 - Fun")
        em.add_field(name = "‎", value = "🔐 - Caesarcrypt\n🔍 - VirusTotal\n🔄 - Update\n👑 - Admin\n❓ - About")
        embedmsg = await ctx.send(embed=em)
        await embedmsg.add_reaction("🏠")
        await embedmsg.add_reaction("⚔️")
        await embedmsg.add_reaction("⚙️")
        await embedmsg.add_reaction("🪛")
        await embedmsg.add_reaction("😄")
        await embedmsg.add_reaction("🔐")
        await embedmsg.add_reaction("🔍")
        await embedmsg.add_reaction("🔄")
        await embedmsg.add_reaction("👑")
        await embedmsg.add_reaction("❓")

        latestversionresponse = requests.get("https://api.github.com/repos/FOSS-Devs/fossdiscord/releases/latest")
        latestversionget = latestversionresponse.json()["name"]
        latestversion = "6.1.3"
        secondem = discord.Embed(title = "Help", color = discord.Color.red())
        secondem.add_field(name = "Options", value = "🏠 - Home (this page)\n⚔️ - Moderation\n⚙️ - Settings\n🪛 - Utils\n😄 - Fun")
        secondem.add_field(name = "‎", value = "🔐 - Caesarcrypt\n🔍 - VirusTotal\n🔄 - Update\n👑 - Admin\n❓ - About")
        if globalconfig.currentversion == latestversion:
            secondem.add_field(name = "Updates", value = "FOSSDiscord Discord.py is DEPRECATED! https://github.com/FOSS-Devs/fossdiscord-new", inline=False)
        elif globalconfig.currentversion > latestversion:
            secondem.add_field(name = "Updates", value = f"FOSSDiscord Discord.py is DEPRECATED! https://github.com/FOSS-Devs/fossdiscord-new", inline=False)
        else:
            secondem.add_field(name = "Updates", value = f"You can update the bot from {globalconfig.currentversion} to {latestversion}.\nCheck the changelog with {config.prefix}updatecheck.\nUpdate with {config.prefix}updatebot.", inline=False)
        await embedmsg.edit(embed=secondem)
        def check(reaction, user):
            return embedmsg == reaction.message
        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=300)
            except asyncio.TimeoutError:
                secondem = discord.Embed(title = "Timed out", description = "To prevent high resource usage, I've suspended this embed.", color = discord.Color.orange())
                await embedmsg.edit(embed=secondem)
                await embedmsg.clear_reaction("🏠")
                await embedmsg.clear_reaction("⚔️")
                await embedmsg.clear_reaction("⚙️")
                await embedmsg.clear_reaction("🪛")
                await embedmsg.clear_reaction("😄")
                await embedmsg.clear_reaction("🔐")
                await embedmsg.clear_reaction("🔍")
                await embedmsg.clear_reaction("🔄")
                await embedmsg.clear_reaction("👑")
                await embedmsg.clear_reaction("❓")
                break
            else:
                if str(reaction.emoji) == "🏠":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title = "Help", color = discord.Color.red())
                    secondem.add_field(name = "Options", value = "🏠 - Home (this page)\n⚔️ - Moderation\n⚙️ - Settings\n🪛 - Utils\n😄 - Fun")
                    secondem.add_field(name = "‎", value = "🔐 - Caesarcrypt\n🔍 - VirusTotal\n🔄 - Update\n👑 - Admin\n❓ - About")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("🏠", user)

                    latestversionresponse = requests.get("https://api.github.com/repos/FOSS-Devs/fossdiscord/releases/latest")
                    latestversionget = latestversionresponse.json()["name"]
                    latestversion = "6.1.3"
                    secondem = discord.Embed(title = "Help", color = discord.Color.red())
                    secondem.add_field(name = "Options", value = "🏠 - Home (this page)\n⚔️ - Moderation\n⚙️ - Settings\n🪛 - Utils\n😄 - Fun")
                    secondem.add_field(name = "‎", value = "🔐 - Caesarcrypt\n🔍 - VirusTotal\n🔄 - Update\n👑 - Admin\n❓ - About")
                    if globalconfig.currentversion == latestversion:
                        secondem.add_field(name = "Updates", value = "FOSSDiscord Discord.py is DEPRECATED! https://github.com/FOSS-Devs/fossdiscord-new", inline=False)
                    elif globalconfig.currentversion > latestversion:
                        secondem.add_field(name = "Updates", value = f"FOSSDiscord Discord.py is DEPRECATED! https://github.com/FOSS-Devs/fossdiscord-new", inline=False)
                    else:
                        secondem.add_field(name = "Updates", value = f"You can update the bot from {globalconfig.currentversion} to {latestversion}.\nCheck the changelog with {config.prefix}updatecheck.\nUpdate with {config.prefix}updatebot.", inline=False)
                    await embedmsg.edit(embed=secondem)

                if str(reaction.emoji) == "⚔️":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title = "Help", description = "Use `" + config.prefix + "help <command>` for extended information on a command.", color = discord.Color.blue())
                    secondem.add_field(name = "Moderation", value = "ban\nchangenick\ndelwarning\nkick\nmodnick\nmute\npurge\nunban\nunmute\nwarn\nwarnings")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("⚔️", user)

                if str(reaction.emoji) == "⚙️":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title="Help", description="Use `" + config.prefix + "help <command>` for extended information on a command.", color=discord.Color.blue())
#
#                   Changelog:
#                   Fixed the old bugs.Embed(title = "Help", description = "Use `" + config.prefix + "help <command>` for extended information on a command.", color = discord.Color.blue())
#                   secondem.add_field(name = "Settings", value = "botstatus\nbotstatusrepeat\nsettings")
                    secondem.add_field(name = "Settings", value = "bot\nfilter\nlogging\ndateformat")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("⚙️", user)

                if str(reaction.emoji) == "🪛":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title = "Help", description = "Use `" + config.prefix + "help <command>` for extended information on a command.", color = discord.Color.blue())
                    secondem.add_field(name = "Utils", value = "about\navatar\njoined\nping\nquickpoll\nuptime\nuserinfo")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("🪛", user)

                if str(reaction.emoji) == "😄":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title = "Help", description = "Use `" + config.prefix + "help <command>` for extended information on a command.", color = discord.Color.blue())
                    secondem.add_field(name = "Fun", value = "cat\nchoose\ndog\nemote\nf")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("😄", user)

                if str(reaction.emoji) == "🔐":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title = "Help", description = "Use `" + config.prefix + "help <command>` for extended information on a command.", color = discord.Color.blue())
                    secondem.add_field(name = "Caesarcrypt", value = "twisted_msg\nuntwisted_msg")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("🔐", user)

                if str(reaction.emoji) == "🔍":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title = "Help", description = "Use `" + config.prefix + "help <command>` for extended information on a command.", color = discord.Color.blue())
                    secondem.add_field(name = "VirusTotal", value = "scanurl\nrescan")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("🔍", user)

                if str(reaction.emoji) == "🔄":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title = "Help", description = "Use `" + config.prefix + "help <command>` for extended information on a command.", color = discord.Color.blue())
                    secondem.add_field(name = "Update", value = "updatecheck\nupdatebot")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("🔄", user)

                if str(reaction.emoji) == "👑":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title = "Help", description = "Use `" + config.prefix + "help <command>` for extended information on a command.", color = discord.Color.blue())
                    secondem.add_field(name = "Admin", value = "blacklist\ngetchannels\ngetinvite\nloadcog\nreloadcog\nservers\nshutdownbot\nunloadcog")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("👑", user)

                if str(reaction.emoji) == "❓":
                    if user.name == self.bot.user.name:
                        continue
                    secondem = discord.Embed(title = "Help", description = "Use `" + config.prefix + "help <command>` for extended information on a command.", color = discord.Color.blue())
                    secondem.add_field(name = "About", value = "about\nhelp")
                    await embedmsg.edit(embed=secondem)
                    await embedmsg.remove_reaction("❓", user)

    # Moderation commands
    @help.command(name="ban")
    async def _ban(self, ctx):
        em = discord.Embed(title = "Moderation: Ban", description = config.prefix + "ban <user> optional:<reason> \n\nBan a member.", color = discord.Color.blue())
        await ctx.send(embed = em)
    
    @help.command(name="changenick")
    async def _changenick(self, ctx):
        em = discord.Embed(title = "Moderation: ChangeNick", description = config.prefix + "changenick <user ID or mention> <new nickname (if not given the nickname will be reset) \n\nChanges the nickname of a user or a bot.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="delwarning", aliases=['delwarn'])
    async def _delwarning(self, ctx):
        em = discord.Embed(title = "Moderation: Delwarning", description = config.prefix + "delwarning <user> <casenumber or `all`> \n\nDelete a warning.\nAliases: delwarn", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="kick")
    async def _kick(self, ctx):
        em = discord.Embed(title = "Moderation: Kick", description = config.prefix + "kick <user> optional:<reason> \n\nKick a member.", color = discord.Color.blue())
        await ctx.send(embed = em)
    
    @help.command(name="modnick")
    async def _modnick(self, ctx):
        em = discord.Embed(title = "Moderation: ModNick", description = config.prefix + 'modnick <user ID or mention>\n\nModerates the nickname of a user or a bot (sets the nickname to "ModdedNick-(random letters and numbers)".', color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="mute")
    async def _mute(self, ctx):
        em = discord.Embed(title = "Moderation: Mute", description = config.prefix + "mute <user> <mutetime> \n\nMute a member.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="purge")
    async def _purge(self, ctx):
        em = discord.Embed(title = 'Moderation: Purge:', color = discord.Color.blue())
        em.add_field(name = f"{config.prefix}purge <number of messages to purge>", value="Purge certain amount of messages.")
        em.add_field(name = f"{config.prefix}purge <user> <how many messages to look back for message sent by user>", value="Purge certain amount of messages sent by a certain user.")

    @help.command(name="unban")
    async def _unban(self, ctx):
        em = discord.Embed(title = "Moderation: Unban", description = config.prefix + "unban <userid> \n\nUnban a member.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="unmute")
    async def _unmute(self, ctx):
        em = discord.Embed(title = "Moderation: Unmute", description = config.prefix + "unmute <user> \n\nUnmute a member.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="warn")
    async def _warn(self, ctx):
        em = discord.Embed(title = "Moderation: Warn", description = config.prefix + "warn <user> <reason> \n\nWarn a member.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="warnings", aliases=['warns'])
    async def _warnings(self, ctx):
        em = discord.Embed(title = "Moderation: Warnings", description = config.prefix + "warnings <user> \n\nSee the warnings for a member.\nAliases: warns", color = discord.Color.blue())
        await ctx.send(embed = em)

    # General commands
    @help.command(name="about")
    async def _about(self, ctx):
        em = discord.Embed(title = "General: About", description = config.prefix + "about \n\nShows information about this bot instance.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="choose")
    async def _choose(self, ctx):
        em = discord.Embed(title = "Fun: Choose", description = config.prefix + "choose "<choice1>" "<choice2>" \n\nChooses between multiple choices.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="f")
    async def _f(self, ctx):
        em = discord.Embed(title = "Fun: F", description = config.prefix + "f <message> \n\nSays F in the chat and adds an F emoji to the message.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="cat")
    async def _cat(self, ctx):
        em = discord.Embed(title = "Fun: Cat", description = config.prefix + "cat \n\nGet a cat picture.\nAliases: kat, cats, kitten", color = discord.Color.blue())
        await ctx.send(embed = em)
    
    @help.command(name="dog")
    async def _dog(self, ctx):
        em = discord.Embed(title = "Fun: Dog", description = config.prefix + "dog \n\nGet a dog picture.\nAliases: puppy, doggo", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="wikipedia")
    async def _wikipedia(self, ctx):
        em = discord.Embed(title = "Fun: Wikipedia", description = config.prefix + "wiki <something> \n\nGet information about something.", color = discord.Color.blue())
        await ctx.send(embed = em)

    # Settings commands
    #@help.command(name="botstatus")
    #async def _botstatus(self, ctx):
    #    em = discord.Embed(title = "Settings: Botstatus", description = config.prefix + "botstatus <status> \n\nSets the status of the bot. Owner only. '" + config.prefix + "botstatus' to reset", color = discord.Color.blue())
    #    await ctx.send(embed = em)

    @help.command(name="settings")
    async def _settings(self, ctx):
        em = discord.Embed(title = "Settings: Settings", description = config.prefix + "settings \n\nbot\nfilter\nlogging\ndateformat", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="blacklist")
    async def _blacklist(self, ctx):
        em = discord.Embed(title = 'Settings: Blacklist', color = discord.Color.blue())
        em.add_field(name = f"{config.prefix}blacklist add <userid>", value="Add a user to the blacklist. Owner only.")
        em.add_field(name = f"{config.prefix}blacklist remove <userid>", value="Remove a user from the blacklist. Owner only.")
        await ctx.send(embed = em)

    #@help.command(name="botstatusrepeat")
    #async def _botstatusrepeat(self, ctx):
    #    em = discord.Embed(title = "Settings: BotStatusRepeat", description = config.prefix + "botstatusrepeat \n\nRepeatedly sets the status of the bot. Owner only.", color = discord.Color.blue())
    #    await ctx.send(embed = em)

    #bot, filter, blacklist, logging, dateformat

    @help.command(name="bot")
    async def _bot(self, ctx):
        em = discord.Embed(title = "Settings: Bot", description = config.prefix + "settings bot on/off\n\nDisable or enable the bot.", color = discord.Color.blue())
        await ctx.send(embed = em)


    @help.command(name="filter")
    async def _filter(self, ctx):
        em = discord.Embed(title = "Settings: Filter", description = config.prefix + "settings filter on/off\n\nToggle the profanity filter.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="logging")
    async def _logging(self, ctx):
        em = discord.Embed(title = "Settings: Logging", description = config.prefix + "settings logging <channel ID>\n\nSet the logging channel to log events to.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="dateformat")
    async def _dateformat(self, ctx):
        em = discord.Embed(title = "Settings: dateformat", description = config.prefix + "To select the date format of the bot.", color = discord.Color.blue())
        await ctx.send(embed = em)


    # Utils commands
    @help.command(name="avatar")
    async def _avatar(self, ctx):
        em = discord.Embed(title = "Utils: Avatar", description = config.prefix + "avatar <user> \n\nGet a link to somebody's avatar.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="joined")
    async def _joined(self, ctx):
        em = discord.Embed(title = "Utils: Joined", description = config.prefix + "joined <user> \n\nTells you when a user joined the server.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="ping")
    async def _ping(self, ctx):
        em = discord.Embed(title = "Utils: Ping", description = config.prefix + "ping \n\nTells you the latency between the bot and the server.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="quickpoll")
    async def _quickpoll(self, ctx):
        em = discord.Embed(title = "Utils: Quickpoll", description = config.prefix + "quickpoll <poll> \n\nMake a poll with yes/no reactions.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="uptime")
    async def _uptime(self, ctx):
        em = discord.Embed(title = "Utils: Uptime", description = config.prefix + "uptime \n\nShows the uptime of the bot.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="userinfo")
    async def _userinfo(self, ctx):
        em = discord.Embed(title = "Utils: Userinfo", description = config.prefix + "userinfo <user> \n\nGives you information about a user.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="emote")
    async def _emote(self, ctx):
        em = discord.Embed(title = "Utils: Emote", description = config.prefix + "emote <:emote:> \n\nGet info about an emote.", color = discord.Color.blue())
        await ctx.send(embed = em)

    # Caesar commands
    @help.command(name="twisted_msg")
    async def _encrypt(self, ctx):
        em = discord.Embed(title = "Caesarcrypt: Twisted Your Message", description = config.prefix + "twisted_msg <rounds> <message> \n\nTwisted a message.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="untwisted_msg")
    async def _decrypt(self, ctx):
        em = discord.Embed(title = "Caesarcrypt: Untwisted Your Message", description = config.prefix + "untwisted_msg <rounds> <message> \n\nUntwisted a message.", color = discord.Color.blue())
        await ctx.send(embed = em)

    # Update commands
    @help.command(name="updatebot")
    async def _updatebot(self, ctx):
        em = discord.Embed(title = "Update: UpdateBot", description = config.prefix + "updatebot \n\nUpdates the bot. Owner only.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="updatecheck")
    async def _updatecheck(self, ctx):
        em = discord.Embed(title = "Update: UpdateCheck", description = config.prefix + "updatecheck \n\nChecks for updates for the bot. Owner only.", color = discord.Color.blue())
        await ctx.send(embed = em)

    # VirusTotal commands
    @help.command(name="scanurl", aliases=['checkurl','urlcheck','scan_url'])
    async def _scanurl(self, ctx):
        em = discord.Embed(title = "VirusTotal: Scan URL", description = config.prefix + "scanurl <link> \n\nScans a URL through VirusTotal.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="rescan", aliases=['vt_hash', 'recheckfile', 'vthash'])
    async def _rescan(self, ctx):
        em = discord.Embed(title = "VirusTotal: Re-analyze File", description = config.prefix + "rescan <file hash> SHA-256 SHA-1 or MD5 \n\nRe-analyzing a known file through VirusTotal.\nAliases: vt_hash, recheckfile. vthash", color = discord.Color.blue())
        await ctx.send(embed = em)

    # Owner commands
    @help.command(name="loadcog")
    async def _reloadcog(self, ctx):
        em = discord.Embed(title = "Owner: LoadCog", description = config.prefix + "loadcog <cog> \n\nLoads the user specified cog. Owner only.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="lockdownbot")
    async def _lockdownbot(self, ctx):
        em = discord.Embed(title = "Owner: LockdownBot", description = config.prefix + "lockdownbot \n\nLocks down the bot in all servers and disables most commands. Owner only.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="reloadcog")
    async def _reloadcog(self, ctx):
        em = discord.Embed(title = "Owner: ReloadCog", description = config.prefix + "reloadcog <cog> \n\nReloads the user specified cog. Owner only.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="restartbot")
    async def _restartbot(self, ctx):
        em = discord.Embed(title = "Owner: RestartBot", description = config.prefix + "restartbot \n\nRestarts the bot. Owner only.\nAliases: restart", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="shutdownbot")
    async def _shutdownbot(self, ctx):
        em = discord.Embed(title = "Owner: ShutdownBot", description = config.prefix + "shutdownbot \n\nShuts down the bot. Owner only.\nAliases: shutdown", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="unloadcog")
    async def _reloadcog(self, ctx):
        em = discord.Embed(title = "Owner: UnloadCog", description = config.prefix + "unloadcog <cog> \n\nUnloads the user specified cog. Owner only.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="servers")
    async def _servers(self, ctx):
        em = discord.Embed(title = "Owner: Servers", description = config.prefix + "servers \n\nProvides a list of servers the bot is in, along with server IDs. Owner only.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="getchannels")
    async def _getchannels(self, ctx):
        em = discord.Embed(title = "Owner: GetChannels", description = config.prefix + "getchannels <serverid> \n\nGets the channels of the server provided. The bot must be in the server for this to work. Owner only.", color = discord.Color.blue())
        await ctx.send(embed = em)

    @help.command(name="getinvite")
    async def _getinvite(self, ctx):
        em = discord.Embed(title = "Owner: GetInvite", description = config.prefix + "getinvite <serverid> <channel>\n\nGenerates an invite for the server provided. A channel name can optionally be provided and it defauts to `general`. Owner only.", color = discord.Color.blue())
        await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Help(bot))
