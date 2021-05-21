import discord, time
from discord.ext import commands
import config
import json, base64, requests, asyncio

apikey = config.virustotal_api

def vt_json_parsing(detections):
    try:
        detections = str(detections).split("last_analysis_stats")
        detections = str(detections[1]).split('"')
    except Exception:
        return -1
    for m in detections:
        if 'malicious' in str(m) and any(d.isdigit() for d in m):
            detections = m
            detections = "".join(filter(str.isdigit, m))
            break
    return detections

class VT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vt_hash(self, ctx, hash: str):
        """VirusTotal Integration"""
        if config.bot_lockdown_status == 'no_lockdown':
            header = {'x-apikey': '{}'.format(apikey)}
            vturl = "https://www.virustotal.com/api/v3/files/{}".format(hash)
            response = requests.get(vturl, headers = header).json()
            response = str(response).split(",")
            parsed = vt_json_parsing(response)
            if parsed == -1:
                em = discord.Embed(title = "Something went wrong.")
                await ctx.send(embed = em)
            else:
                em = discord.Embed(title = "Detections: {}".format(parsed))
                await ctx.send(embed = em)
        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)

    @commands.command()
    async def scan_url(self, ctx, url: str):
        #Need to import base64 module to work
        await ctx.message.delete()
        if config.bot_lockdown_status == 'no_lockdown':
            header = {'x-apikey': '{}'.format(apikey)}
            data = {'url': url}
            vturl = "https://www.virustotal.com/api/v3/urls"
            response = requests.post(vturl, data = data, headers = header).json()
            response = str(response).split(",")
            keyword = "'id': '"
            for i in response:
                if keyword in str(i):
                    response = i.replace(keyword, "").replace("}", "").replace("'", "").replace(" ", "").split("-")
                    try:
                        result_id = str(response[1])
                    except Exception:
                        em = discord.Embed(title = "Something went wrong. Could be that you did not add the http/https prefix at the beginning of the webpage.")
                        await ctx.send(embed = em)
                        return
                    break
            try:
                vturl = "https://www.virustotal.com/api/v3/urls/{}".format(result_id)
            except Exception:
                em = discord.Embed(title = "Something went wrong.")
                await ctx.send(embed = em)
                return
            em = discord.Embed(title = "Analyzing url...", description = "Please wait for 15 seconds.")
            await ctx.send(embed = em)
            await asyncio.sleep(15)
            response = requests.get(vturl, headers=header).json()
            response = str(response).split(",")
            parsed = vt_json_parsing(response)
            if parsed == -1:
                em = discord.Embed(title = "Something went wrong. Could be that you did not add the http/https prefix at the beginning of the webpage.")
                await ctx.send(embed = em)
            else:
                generated_link = "https://www.virustotal.com/gui/url/{}/detection".format(result_id)
                em = discord.Embed(title = "Detections: {}".format(str(parsed)))
                em.add_field(name="Link:", value=generated_link)
                await ctx.send(embed = em)
        elif config.bot_lockdown_status == "lockdown_activated":
            em = discord.Embed(title = "This bot is locked down", description = "<@!" + config.ownerID + "> has locked down this bot globally.")
            await ctx.send(embed = em)

def setup(bot):
    bot.add_cog(VT(bot))
