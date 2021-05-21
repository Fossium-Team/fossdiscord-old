import discord
from discord.ext import commands
import config
import datetime
import time
start_time = time.time()
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        '''
        Get the latency of the bot.
        '''
        if config.bot_lockdown_status == 'no_lockdown':
            em = discord.Embed(title = "Pong! `"f"{round(self.bot.latency*1000)} ms`.")
            await ctx.send(embed = em)
        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)

    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Get a link to somebody's avatar."""
        if config.bot_lockdown_status == 'no_lockdown':
            if user is None:
                user = ctx.author
                await ctx.send(user.avatar_url)
            else:
                await ctx.send(user.avatar_url)
        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """Gives information about a user."""
        if config.bot_lockdown_status == 'no_lockdown':
            if user is None:
                user = ctx.author
                if user.display_name == user.name:
                    usernickname = "None"
                else:
                    usernickname = user.display_name
                date_format = "%d/%m/%Y, %I:%M %p"
                embed = discord.Embed()
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
            else:
                if user.display_name == user.name:
                    usernickname = "None"
                else:
                    usernickname = user.display_name
                date_format = "%d/%m/%Y, %I:%M %p"
                embed = discord.Embed()
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
        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        """Says when a member joined."""
        if config.bot_lockdown_status == 'no_lockdown':
            em = discord.Embed(title = '{0.name} joined in {0.joined_at}'.format(member))
            await ctx.send(embed = em)
        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)


    @commands.command()
    async def serverinfo(self, ctx):
        """Gives some information about the server."""
        if config.bot_lockdown_status == 'no_lockdown':
            name = str(ctx.guild.name)
            description = str(ctx.guild.description)

            owner = str(ctx.guild.owner)
            id = str(ctx.guild.id)
            region = str(ctx.guild.region)
            memberCount = str(ctx.guild.member_count)
            icon = str(ctx.guild.icon_url)
            embed = discord.Embed(
                title=name + " Server Information",
                description=description,
                color=discord.Color.blue()
                )
            embed.set_thumbnail(url=icon)
            embed.add_field(name="Owner", value=owner, inline=True)
            embed.add_field(name="Server ID", value=id, inline=True)
            embed.add_field(name="Region", value=region, inline=True)
            embed.add_field(name="Member Count", value=memberCount, inline=True)

            await ctx.send(embed=embed)
        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)

    @commands.command()
    async def quickpoll(self, ctx, *poll):
        if config.bot_lockdown_status == 'no_lockdown':
            args = " ".join(poll[:])
            em = discord.Embed(title = f'{args}')
            msg = await ctx.send(embed = em)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)

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

def setup(bot):
    bot.add_cog(Utils(bot))
