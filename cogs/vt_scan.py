# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord, time, json, base64, requests, asyncio
from discord.ext import commands
import config

apikey = config.virustotal_api
iconurl = "https://raw.githubusercontent.com/FOSS-Devs/fossdiscord/main/src/vt_logo.png"

def vt_json_parsing(detections):
    try:
        detections = str(detections).split("last_analysis_stats")
        detections = str(detections[1]).split('"')
    except Exception:
        return -1
    for m in detections:
        if 'malicious' in str(m) and any(d.isdigit() for d in m):
            #detections = m
            detections = "".join(filter(str.isdigit, m))
            break
    return detections

class VT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hashcheck', 'checkhash'])
    async def vt_hash(self, ctx, hash: str):
        """VirusTotal Integration"""
        await ctx.message.delete()
        header = {'x-apikey': '{}'.format(apikey)}
        vturl = "https://www.virustotal.com/api/v3/files/{}".format(hash)
        response = requests.get(vturl, headers = header).json()
        response = str(response).split(",")
        parsed = vt_json_parsing(response)
        if parsed == -1:
            em = discord.Embed(title = "Something went wrong, could be the hash not in the VirusTotal database.", color = discord.Color.red())
            em.set_author(name="VirusTotal", icon_url=iconurl)
            await ctx.send(embed = em)
            return
        else:
            generated_link = "https://www.virustotal.com/gui/file/{}/detection".format(hash)
            if int(parsed) == 0 :
                em = discord.Embed(title = "Detections: {}".format(parsed), color = discord.Color.green())
            elif int(parsed) >= 1 :
                em = discord.Embed(title = "Detections: {}".format(parsed), color = discord.Color.red())
            em.set_author(name="VirusTotal", icon_url=iconurl)
            em.add_field(name="Link:", value=generated_link)
            await ctx.send(embed = em)
            return


    @commands.command(alias=['checkurl','urlcheck','scanurl'])
    async def scan_url(self, ctx, url: str):
        #Need to import base64 module to work
        await ctx.message.delete()
        header = {'x-apikey': '{}'.format(apikey)}
        data = {'url': url}
        vturl = "https://www.virustotal.com/api/v3/urls"
        response = requests.post(vturl, data = data, headers = header).json()
        try:
            result_id = str(response['data']['id']).split('-')[1]
        except Exception:
            response = str(response['error']['code'])
            em = discord.Embed(title = f"Error: '{response}'", color = discord.Color.red())
            em.set_author(name="VirusTotal", icon_url=iconurl)
            await ctx.send(embed = em)
            return
        vturl = f"https://www.virustotal.com/api/v3/urls/{result_id}"
        em = discord.Embed(title = "Analyzing URL...", description = "Please wait for 15 seconds.", color = discord.Color.blue())
        em.set_author(name="VirusTotal", icon_url=iconurl)
        msg = await ctx.send(embed = em)
        await asyncio.sleep(15)
        response = requests.get(vturl, headers=header).json()
        try:
            detection = int(response['data']['attributes']['last_analysis_stats']['malicious'])
        except Exception:
            response = str(response['error']['code'])
            new_embed = discord.Embed(title = f"Error: '{response}'", color = discord.Color.red())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            await msg.edit(embed=new_embed)(embed = em)
            return
        generated_link = "https://www.virustotal.com/gui/url/{}/detection".format(result_id)
        if detection >= 1:
            new_embed = discord.Embed(title = f"Detections: {detection}", color = discord.Color.red())
        else:
            new_embed = discord.Embed(title = f"Detections: {detection}", color = discord.Color.green())
        new_embed.set_author(name="VirusTotal", icon_url=iconurl)
        new_embed.add_field(name="Link:", value=generated_link)
        await msg.edit(embed=new_embed)


def setup(bot):
    bot.add_cog(VT(bot))
