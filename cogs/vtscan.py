# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord, time, json, base64, requests, asyncio
from discord.ext import commands
import config

apikey = config.virustotal_api
iconurl = "https://raw.githubusercontent.com/FOSS-Devs/fossdiscord/main/src/vt_logo.png"

class VT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 45, commands.BucketType.guild)
    @commands.command(aliases=['hashcheck', 'checkhash'])
    async def vt_hash(self, ctx, *, hash: str):
        """VirusTotal Integration"""
        await ctx.message.delete()
        hash = hash.replace(' ', '')
        header = {'x-apikey': f'{apikey}'}
        vturl = f"https://www.virustotal.com/api/v3/files/{hash}"
        response = requests.get(vturl, headers = header).json()
        try:
            detection = int(response['data']['attributes']['last_analysis_stats']['malicious'])
            suspicious = int(response['data']['attributes']['last_analysis_stats']['suspicious'])
        except Exception:
            response = str(response['error']['code'])
            em = discord.Embed(title = f"Error: `{response}`", color = discord.Color.red())
            em.set_author(name="VirusTotal", icon_url=iconurl)
            await ctx.send(embed = em, delete_after=5.0)
            return
        generated_link = f"https://www.virustotal.com/gui/file/{hash}/detection"
        if detection >= 1 or suspicious >= 1:
            em = discord.Embed(title = f"Detections: `{detection}`\nDetected as suspicious: `{suspicious}`", color = discord.Color.red())
        else:
            em = discord.Embed(title = f"The file looks clean, detections: {detection}", color = discord.Color.green())
        em.set_author(name="VirusTotal", icon_url=iconurl)
        em.add_field(name="Link:", value=generated_link)
        await ctx.send(embed = em)

    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    @commands.cooldown(1, 45, commands.BucketType.user)
    @commands.command(aliases=['checkurl','urlcheck','scanurl'])
    async def scan_url(self, ctx, *, url: str):
        #Need to import base64 module to work
        await ctx.message.delete()
        url = url.replace(' ', '')
        header = {'x-apikey': f'{apikey}'}
        data = {'url': url}
        vturl = "https://www.virustotal.com/api/v3/urls"
        response = requests.post(vturl, data = data, headers = header).json()
        try:
            result_id = str(response['data']['id']).split('-')[1]
        except Exception:
            response = str(response['error']['code'])
            em = discord.Embed(title = f"Error: `{response}`", color = discord.Color.red())
            em.set_author(name="VirusTotal", icon_url=iconurl)
            await ctx.send(embed = em, delete_after=5.0)
            return
        vturl = f"https://www.virustotal.com/api/v3/urls/{result_id}"
        em = discord.Embed(title = "Analyzing URL...", description = "Please wait for 15 seconds.", color = discord.Color.blue())
        em.set_author(name="VirusTotal", icon_url=iconurl)
        msg = await ctx.send(embed = em)
        await asyncio.sleep(15)
        response = requests.get(vturl, headers=header).json()
        try:
            detection = int(response['data']['attributes']['last_analysis_stats']['malicious'])
            suspicious = int(response['data']['attributes']['last_analysis_stats']['suspicious'])
        except Exception:
            response = str(response['error']['code'])
            new_embed = discord.Embed(title = f"Error: `{response}`", color = discord.Color.red())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            await msg.edit(embed=new_embed, delete_after=5.0)
            return
        generated_link = f"https://www.virustotal.com/gui/url/{result_id}/detection"
        if detection >= 1 or suspicious >= 1:
            new_embed = discord.Embed(title = f"Detections: `{detection}`\nDetected as suspicious: `{suspicious}`", color = discord.Color.red())
            category = response['data']['attributes']["categories"]
            for attr, value in category.items():
                new_embed.add_field(name = f"{attr}", value = f"`{value}`")
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            new_embed.add_field(name="Link:", value=generated_link)
        else:
            new_embed = discord.Embed(title = f"Detections: `{detection}`, the website should be clean.", color = discord.Color.green())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            new_embed.add_field(name="Link:", value=generated_link)
        await msg.edit(embed=new_embed)


def setup(bot):
    bot.add_cog(VT(bot))
