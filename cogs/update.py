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
#import socket
import wget 

'''def close_port():
        message = 'disconnect'
        host = '127.0.0.1'
        port = 18265
        _socket = socket.socket()
        _socket.connect((host,port))
        _socket.send(message.encode())
        _socket.close()'''

# Thanks for reoccurcat btw for this amazing update command
class Update(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def updatecheck(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
            em = discord.Embed(title = "This command is in development", color = discord.Color.red())
            await ctx.send(embed = em)
        #     # username = os.getlogin()
        #     if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        #         tmpdir = "/tmp"
        #     elif sys.platform == "win32":
        #         tmpdir = "/Temp"
        #     with open('config.py') as f:
        #         if not 'latest_version' in f.read():
        #             with open('config.py', 'a') as writeFile :
        #                 writeFile.write("latest_version = 'unknown'")
        #                 writeFile.close()
        #                 importlib.reload(config)
        #     if not os.path.exists(tmpdir + '/updatecheck'):
        #         os.makedirs(tmpdir + '/updatecheck')
        #     elif os.path.exists(tmpdir + '/updatecheck'):
        #         if os.path.exists(tmpdir + '/updatecheck/.git/objects/pack'):
        #             new_name = str("unlock")
        #             os.rename(tmpdir + '/updatecheck/.git/objects/pack', new_name)
        #             shutil.rmtree('unlock')
        #         shutil.rmtree(tmpdir + '/updatecheck')
        #     #os.mkdir('/tmp/freeupdate')
        #     HTTPS_REMOTE_URL = globalconfig.github_login_url
        #     first_embed = discord.Embed(title = "Checking for updates...", description = "FreeDiscord is now checking for updates. Please be patient.", color = discord.Color.orange())
        #     # send a first message with an embed
        #     msg = await ctx.send(embed=first_embed)
        #     DEST_NAME = tmpdir + '/updatecheck'
        #     cloned_repo = Repo.clone_from(HTTPS_REMOTE_URL, DEST_NAME)
        #     dir_path = os.getcwd()
        #     copyfile(tmpdir + '/updatecheck/globalconfig.py', dir_path + '/updateconfig.py')
        #     try:
        #         shutil.rmtree(tmpdir + '/updatecheck')
        #     except os.error:
        #         embed = discord.Embed(title = "Error in removing `" + tmpdir + "/updatecheck` folder", description = 'The `' + tmpdir + '/updatecheck` folder was not able to be removed, probably due to a permissions issue.', color = discord.Color.red())
        #         await ctx.send(embed=embed) 
        #     import updateconfig
        #     if updateconfig.version > globalconfig.version:
        #         new_embed = discord.Embed(title = "Checking for updates...", description = "Checking for updates succeeded!", color = discord.Color.green())
        #         new_embed.add_field(name = "Upgrade found!", value = "It is recommended to update to version " + updateconfig.version + " from version " + globalconfig.version + " for the latest bug fixes and feature improvements.")
        #         new_embed.add_field(name = "How do I upgrade?", value = "Use `" + config.prefix + "help updatebot` for more details.")
        #         await msg.edit(embed=new_embed)
        #     if updateconfig.version < globalconfig.version:
        #         new_embed = discord.Embed(title = "Checking for updates...", description = "Checking for updates succeeded!", color = discord.Color.green())
        #         new_embed.add_field(name = "Downgrade found!", value = "It is recommended to downgrade to version " + updateconfig.version + " from version " + globalconfig.version + " because something most likely broke in the latest release.")
        #         new_embed.add_field(name = "How do I downgrade?", value = "Use `" + config.prefix + "help updatebot` for more details. (The update command also downgrades the bot.)")
        #         await msg.edit(embed=new_embed)
        #     if updateconfig.version == globalconfig.version:
        #         new_embed = discord.Embed(title = "Checking for updates...", description = "Checking for updates succeeded!", color = discord.Color.green())
        #         new_embed.add_field(name = "No updates found!", value = "You are up to date! This bot is at version `" + globalconfig.version + "` and the latest bot files available are at version `" + updateconfig.version + "`.")
        #         new_embed.add_field(name = "How do I upgrade?", value = "You don't need to take any action, as you are up to date already. However, you can use `" + config.prefix + "help updatebot` for more details about the upgrade/downgrade process.")
        #         await msg.edit(embed=new_embed)
        #     with open('config.py', 'r') as file :
        #         filedata = file.read()
        #     newdata = filedata.replace(config.latest_version, updateconfig.version)
        #     with open('config.py', 'w') as file:
        #         file.write(newdata)
        #     file.close()
        #     importlib.reload(config)
        #     os.remove(dir_path + "/updateconfig.py")

        else:
            em = discord.Embed(title = "This command is for the bot owner only.", color = discord.Color.red())
            await ctx.send(embed = em)

    @commands.command()
    async def updatebot(self, ctx):
        if str(ctx.message.author.id) == config.ownerID:
           if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "win32":
                datetimenow = datetime.now()
                currentdate = datetime.strftime(datetimenow, '%a %b %y %I%M%p')

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

                allfiles = ["bot.py", "setup.py", "cogs", "docs", "src", "README.md", ".gitignore", "LICENSE", "globalconfig.py"]

                for f in allfiles:
                    shutil.move(f'{currentdir}/' + f, f'{currentdir}/backup-{currentdate}')

                allfilesunzipped = os.listdir(f'{currentdir}/updatertemp/unzipped/fossdiscord-{latestversion}')

                for f in allfilesunzipped:
                    shutil.move(f'{currentdir}/updatertemp/unzipped/fossdiscord-{latestversion}/' + f, currentdir)

                shutil.rmtree("updatertemp")
                print("Done! Restart the bot to apply the changes!")
                em = discord.Embed(title = "Updated!", description = "FOSSDiscord updated! No error reported. Check your console to confirm this.", color = discord.Color.green())
                em.add_field(name = "Note", value = "You have to start the bot again manually. If it won't start, open an issue in FOSSDiscord's GitHub repository.")
                await ctx.send(embed = em)
                #close_port()
                await ctx.bot.close()
                subprocess.Popen([f'python3 {currentdir}/bot.py'])
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
