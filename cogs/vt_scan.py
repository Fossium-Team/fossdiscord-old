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
            detections = m
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


    @commands.command()
    async def scan_url(self, ctx, url: str):
        #Need to import base64 module to work
        await ctx.message.delete()
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
                    em = discord.Embed(title = "Something went wrong. Could be that you did not add the http/https prefix at the beginning of the webpage.", color = discord.Color.red())
                    em.set_author(name="VirusTotal", icon_url=iconurl)
                    await ctx.send(embed = em)
                    return
                break
        try:
            vturl = "https://www.virustotal.com/api/v3/urls/{}".format(result_id)
        except Exception:
            em = discord.Embed(title = "Something went wrong.", color = discord.Color.red())
            em.set_author(name="VirusTotal", icon_url=iconurl)
            await ctx.send(embed = em)
            return
        em = discord.Embed(title = "Analyzing URL...", description = "Please wait for 15 seconds.", color = discord.Color.blue())
        em.set_author(name="VirusTotal", icon_url=iconurl)
        msg = await ctx.send(embed = em)
        await asyncio.sleep(15)
        response = requests.get(vturl, headers=header).json()
        response = str(response).split(",")
        parsed = vt_json_parsing(response)
        if parsed == -1:
            new_embed = discord.Embed(title = "Something went wrong. Could be that you did not add the http/https prefix at the beginning of the webpage.", color = discord.Color.red())
            #await ctx.send(embed = em)
            await msg.edit(embed=new_embed)
        else:
            generated_link = "https://www.virustotal.com/gui/url/{}/detection".format(result_id)
            if int(parsed) >= 1:
                new_embed = discord.Embed(title = "Detections: {}".format(str(parsed)), color = discord.Color.red())
            else:
                new_embed = discord.Embed(title = "Detections: {}".format(str(parsed)), color = discord.Color.green())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            new_embed.add_field(name="Link:", value=generated_link)
            #await ctx.send(embed = em)
            await msg.edit(embed=new_embed)


def setup(bot):
    bot.add_cog(VT(bot))
