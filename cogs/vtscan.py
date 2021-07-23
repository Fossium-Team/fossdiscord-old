# Copyright (c) 2021 FOSS-Devs
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import time
import json
import base64
import requests
import asyncio
import config

apikey = config.virustotal_api
iconurl = "https://raw.githubusercontent.com/FOSS-Devs/fossdiscord/main/src/vt_logo.png"

class VT(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    @commands.cooldown(1, 45, commands.BucketType.guild)
    @commands.command(aliases=['vthash', 'recheckfile', 'vt_hash'])
    async def rescan(self, ctx, *, hash: str):
        """VirusTotal Integration"""
        await ctx.message.delete()
        hash = hash.replace(' ', '')
        header = {'x-apikey': f'{apikey}'}
        vturl = f'https://www.virustotal.com/api/v3/files/{hash}/analyse'
        response = requests.post(vturl, headers = header).json()
        try:
            result_id = str(response['data']['id'])
        except KeyError:
            response = str(response['error']['code'])
            em = discord.Embed(title = f"Error: `{response}`", color = discord.Color.red())
            em.set_author(name="VirusTotal", icon_url=iconurl)
            await ctx.send(embed = em, delete_after=5.0)
            return
        timer = 80
        em = discord.Embed(title = "Re-analyzing file...", description = f"Please wait for {timer} seconds.", color = discord.Color.blue())
        em.set_author(name="VirusTotal", icon_url=iconurl)
        msg = await ctx.send(embed = em)
        while timer != 0:
            new_embed = discord.Embed(title = "Re-analyzing file...", description = f"Please wait for {timer} seconds.", color = discord.Color.blue())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            await msg.edit(embed=new_embed)
            timer -= 1
            await asyncio.sleep(1)
        vturl = f'https://www.virustotal.com/api/v3/analyses/{result_id}'
        response = requests.get(vturl, headers=header).json()
        try:
            qstatus = response["data"]["attributes"]["status"]
            if qstatus == "queued":
                timer = 80
                while timer != 0:
                    new_embed = discord.Embed(title = f"The task still in queue.", description =f"Please wait {timer} more seconds.", color = discord.Color.orange())
                    new_embed.set_author(name="VirusTotal", icon_url=iconurl)
                    await msg.edit(embed=new_embed)
                    timer -= 1
                    await asyncio.sleep(1)
                response = requests.get(vturl, headers=header).json()
            else:
                pass
        except KeyError:
            response = str(response['error']['code'])
            new_embed = discord.Embed(title = f"Error: `{response}`", color = discord.Color.red())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            await msg.edit(embed=new_embed, delete_after=5.0)
            return
        try:
            detection = int(response['data']['attributes']['stats']['malicious'])
            suspicious = int(response['data']['attributes']['stats']['suspicious'])
        except KeyError:
            response = str(response['error']['code'])
            new_embed = discord.Embed(title = f"Error: `{response}`", color = discord.Color.red())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            await msg.edit(embed=new_embed, delete_after=5.0)
            return
        generated_link = f"https://www.virustotal.com/gui/file/{hash}/detection"
        if detection >= 1 or suspicious >= 1:
            new_embed = discord.Embed(title = "Scan Result:", color = discord.Color.red())
            #new_embed.add_field(name= '\u200B', value= '\u200B', inline = False)
            new_embed.add_field(name="Number of Detections as Malicious:", value=f"{detection}", inline=False)
            new_embed.add_field(name="Number of Detections as Suspicious:", value=f"{suspicious}", inline=False)
        else:
            new_embed = discord.Embed(title = "The file should be clean.", color = discord.Color.green())
        #new_embed.add_field(name= '\u200B', value= '\u200B', inline = False)
        new_embed.set_author(name="VirusTotal", icon_url=iconurl)
        new_embed.add_field(name="Link:", value=generated_link, inline=False)
        await msg.edit(embed=new_embed)

    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    @commands.cooldown(1, 45, commands.BucketType.user)
    @commands.command(aliases=['checkurl','urlcheck','scan_url'])
    async def scanurl(self, ctx, *, url: str):
        #Need to import base64 module to work
        await ctx.message.delete()
        url = url.replace(' ', '')
        header = {'x-apikey': f'{apikey}'}
        data = {'url': url}
        vturl = "https://www.virustotal.com/api/v3/urls"
        response = requests.post(vturl, data = data, headers = header).json()
        try:
            result_id = str(response['data']['id']).split('-')[1]
        except KeyError:
            response = str(response['error']['code'])
            em = discord.Embed(title = f"Error: `{response}`", color = discord.Color.red())
            em.set_author(name="VirusTotal", icon_url=iconurl)
            await ctx.send(embed = em, delete_after=5.0)
            return
        vturl = f"https://www.virustotal.com/api/v3/urls/{result_id}"
        timer = 25
        em = discord.Embed(title = "Analyzing URL...", description = f"Please wait for {timer} seconds.", color = discord.Color.blue())
        em.set_author(name="VirusTotal", icon_url=iconurl)
        msg = await ctx.send(embed = em)
        while timer != 0:
            new_embed = discord.Embed(title = "Analyzing URL...", description = f"Please wait for {timer} seconds.", color = discord.Color.blue())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            await msg.edit(embed=new_embed)
            timer -= 1
            await asyncio.sleep(1)
        response = requests.get(vturl, headers=header).json()
        try:
            detection = int(response['data']['attributes']['last_analysis_stats']['malicious'])
            suspicious = int(response['data']['attributes']['last_analysis_stats']['suspicious'])
        except KeyError:
            response = str(response['error']['code'])
            new_embed = discord.Embed(title = f"Error: `{response}`", color = discord.Color.red())
            new_embed.set_author(name="VirusTotal", icon_url=iconurl)
            await msg.edit(embed=new_embed, delete_after=5.0)
            return
        generated_link = f"https://www.virustotal.com/gui/url/{result_id}/detection"
        if detection >= 1 or suspicious >= 1:
            new_embed = discord.Embed(title = f"Scan Result:", color = discord.Color.red())
            #new_embed.add_field(name= '\u200B', value= '\u200B', inline = False)
            new_embed.add_field(name="Number of Detections as Malicious:", value=f"{detection}", inline=False)
            new_embed.add_field(name="Number of Detections as Suspicious:", value=f"{suspicious}", inline=False)
        else:
            new_embed = discord.Embed(title = "The website should be clean.", color = discord.Color.green())
            #new_embed.add_field(name= '\u200B', value= '\u200B', inline = False)
        category = response['data']['attributes']["categories"]
        count = 0
        for attr, value in category.items():
            count += 1
            if count == len(category):
                new_embed.add_field(name = f"{attr}", value = f"`{value}`", inline=False)
            else:
                new_embed.add_field(name = f"{attr}", value = f"`{value}`", inline=True)
        #new_embed.add_field(name= '\u200B', value= '\u200B', inline = False)
        new_embed.set_author(name="VirusTotal", icon_url=iconurl)
        new_embed.add_field(name="Link:", value=generated_link, inline=False)
        await msg.edit(embed=new_embed)


def setup(bot):
    bot.add_cog(VT(bot))
