import discord
from discord.ext import commands
import psutil
import config
import bot
import datetime
import time
start_time = time.time()

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Shows information about bot instance.')
    async def about(self, ctx):
        em = discord.Embed(title = "About this instance", color = discord.Color.orange())
        em.add_field(name = "Website", value = "https://freediscord.ga")
        em.add_field(name = "Project URL", value = "https://github.com/reoccurdevs/freediscord/")
        em.add_field(name = "Support server", value = "https://discord.gg/BNhVjFyB3S")
        em.add_field(name = "Main bot invite link", value = "https://freediscord.ga/invite")
        servers = list(self.bot.guilds)
        serverNumber = len(servers)
        em.add_field(name = "Number of servers this instance is in", value = serverNumber)
        cpuUsage = psutil.cpu_percent()
        em.add_field(name = "CPU usage of host", value = cpuUsage)
        em.add_field(name = "Ping", value = "`"f"{round(self.bot.latency*1000)} ms`")
        current_time = time.time()
        difference = int(round(current_time - start_time))
        text = str(datetime.timedelta(seconds=difference))
        em.add_field(name="Uptime", value=text)
        await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(General(bot))
