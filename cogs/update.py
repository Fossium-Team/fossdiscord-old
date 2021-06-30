# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import discord
from discord.ext import commands
import os
import shutil
import sys
import subprocess
from stat import S_IREAD, S_IRGRP, S_IROTH, S_IWUSR
from shutil import copyfile
import config
import globalconfig
import importlib
import wget
import time
import re
from zipfile import ZipFile
import requests
from datetime import datetime

# Cross-platform updater
class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def updatecheck(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            firstem = discord.Embed(title = "FOSSDiscord is checking for updates...", color = discord.Color.orange())
            embedmsg = await ctx.send(embed=firstem)
            latestversionresponse = requests.get("https://api.github.com/repos/FOSS-Devs/fossdiscord/releases/latest")
            latestversionget = latestversionresponse.json()["name"]
            latestversion = latestversionget.split(' ', 1)[1]
            if globalconfig.currentversion == latestversion:
                secondem = discord.Embed(title = "Updatecheck\n----------------", color = discord.Color.green())
                secondem.add_field(name = "Checking for updates succeeded!", value = "There are no updates available.")
                await embedmsg.edit(embed=secondem)
            elif globalconfig.currentversion > latestversion:
                secondem = discord.Embed(title = "Updatecheck\n----------------", color = discord.Color.green())
                secondem.add_field(name = "Invalid version in the globalconfig.", value = "There is an invalid version in the globalconfig, try downloading a fresh copy of FOSSDiscord.")
                await embedmsg.edit(embed=secondem)
            else:
                secondem = discord.Embed(title = "Updatecheck\n----------------", color = discord.Color.green())
                secondem.add_field(name = "Checking for updates succeeded!", value = f"The bot can be updated from {globalconfig.currentversion} to {latestversion}.\nYou can update the bot with {config.prefix}updatebot.")
                await embedmsg.edit(embed=secondem)
        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def updatebot(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "win32":
                latestversionresponse = requests.get("https://api.github.com/repos/FOSS-Devs/fossdiscord/releases/latest")
                latestversionget = latestversionresponse.json()["name"]
                latestversion = latestversionget.split(' ', 1)[1]
                if globalconfig.currentversion == latestversion:
                    em = discord.Embed(title = "Updatebot\n-------------", color = discord.Color.green())
                    em.add_field(name = 'Already the latest version.', value = "There is no need to update.")
                    await ctx.send(embed=em)
                elif globalconfig.currentversion > latestversion:
                    em = discord.Embed(title = "Updatebot\n-------------", color = discord.Color.green())
                    em.add_field(name = 'Invalid version in the globalconfig.', value = "There is an invalid version in the globalconfig, try downloading a fresh copy of FOSSDiscord.")
                    await ctx.send(embed=em)
                else:
                    datetimenow = datetime.now()
                    currentdate = datetime.strftime(datetimenow, '%a %b %y %I-%M-%S%p')

                    latestversionresponse = requests.get("https://api.github.com/repos/FOSS-Devs/fossdiscord/releases/latest")
                    latestversionget = latestversionresponse.json()["name"]
                    latestversion = latestversionget.split(' ', 1)[1]

                    downloadurl = f"https://codeload.github.com/FOSS-Devs/fossdiscord/zip/v{latestversion}"
                    currentdir = os.getcwd()

                    os.mkdir(f'{currentdir}/updatertemp')
                    os.mkdir(f'{currentdir}/updatertemp/unzipped')
                    wget.download(downloadurl, f'{currentdir}/updatertemp/download.zip')

                    with ZipFile(f'{currentdir}/updatertemp/download.zip', 'r') as zipObj:
                        zipObj.extractall(f'{currentdir}/updatertemp/unzipped')

                    os.mkdir(f'{currentdir}/backup-{currentdate}')

                    allfiles = ["bot.py", "setup.py", "cogs", "requirements.txt", "src", "README.md", ".gitignore", ".github", "LICENSE", "globalconfig.py"]

                    for f in allfiles:
                        shutil.move(f'{currentdir}/' + f, f'{currentdir}/backup-{currentdate}')

                    allfilesunzipped = os.listdir(f'{currentdir}/updatertemp/unzipped/fossdiscord-{latestversion}')

                    for f in allfilesunzipped:
                        shutil.move(f'{currentdir}/updatertemp/unzipped/fossdiscord-{latestversion}/' + f, currentdir)

                    shutil.rmtree("updatertemp")
                    print("Done! Restart the bot to apply the changes!")
                    em = discord.Embed(title = "Updated!", description = "FOSSDiscord updated! No error reported. Check your console to confirm this.", color = discord.Color.green())
                    em.add_field(name = "Note", value = "The bot should start up again. If it doesn't, try to start the bot manually. If the bot errors while starting, please open an issue in FOSSDiscord's GitHub repository.")
                    await ctx.send(embed = em)
                    #close_port()
                    await ctx.bot.close()
                    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
        elif sys.platform == "darwin":
                em = discord.Embed(title = "We are still testing `updatebot` for macOS.", color = discord.Color.red())
                await ctx.send(embed = em)

        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    # @commands.command()
    # async def updatecogs(self, ctx):
    #     """Updates cogs, but not the bot."""
    #     if str(ctx.message.author.id) == config.ownerID:
    #         # username = os.getlogin()
    #         try:
    #             os.mkdir('/tmp/cogupdate')
    #         except OSError:
    #             os.rmdir('/tmp/cogupdate')
    #             os.mkdir('/tmp/cogupdate')
    #         HTTPS_REMOTE_URL = globalconfig.github_login_url
    #         DEST_NAME = '/tmp/cogupdate'
    #         cloned_repo = Repo.clone_from(HTTPS_REMOTE_URL, DEST_NAME)
    #         dir_path = os.getcwd()
    #         shutil.rmtree(dir_path + "/cogs/")
    #         path = dir_path
    #         src = '/tmp/cogupdate/cogs'
    #         dest = dir_path + "/cogs"
    #         destination = shutil.copytree(src, dest)
    #         shutil.rmtree('/tmp/cogupdate')
    #         print("Done! Restart the bot to apply the changes!")
    #         em = discord.Embed(title = "Updated!", description = "Cogs updated! No error reported. Check your console to confirm this.", color = discord.Color.green())
    #         em.add_field(name = "Note", value = "If you want to use the new cogs, either restart the bot using `" + config.prefix + "restartbot` which will load all the cogs on startup (recommended), or reload every cog manually using `" + config.prefix + "reloadcog {every cog name}.`")
    #         await ctx.send(embed = em)
    #     else:
    #         em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
    #         await ctx.send(embed = em)


def setup(bot):
    bot.add_cog(Update(bot))
