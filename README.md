# FOSSDiscord
## Welcome to the official GitHub page of the FOSSDiscord bot!
FOSSDiscord is a general purpose Discord bot maintained by [SKBotNL](https://github.com/SKBotNL) and [Odysseus](https://github.com/Odysseus443). It is a fork of a bot called FreeDiscord that we used to work on as the reoccurdevs team. As we had disagreements with the owner of the bot, we left the reoccurdevs team and we forked the bot. FreeDiscord is still maintained by the owner and you can find it [here](https://github.com/reoccurcat/freediscord). Our bot is not a continuation of FreeDiscord, it is just based on FreeDiscord. FOSSDiscord will go on its own path. If you find an issue, or have a feature suggestion, please let us know by opening an issue [here](https://github.com/FOSS-Devs/FOSSDiscord/issues).

## Documentation

### Starting the bot
#### Make sure you have [Python 3](https://www.python.org/downloads/) installed (and put in path, if you're on Windows 10)!!!
1. Clone the repository: `git clone https://github.com/FOSS-Devs/FOSSDiscord.git` and go to step 2. An alternative is to download the ZIP file, unzip it, shift + right click in the `FOSSDiscord-main` folder, click on `Open Powershell window here`, and continue with step 3.
2. `cd` to the repository folder: `cd FOSSDiscord`.
3. Make sure all the dependencies are installed, Windows: `python -m pip install discord.py requests asyncio gitpython psutil datetime` Linux: `pip3 install discord.py requests asyncio gitpython psutil datetime`.
4. Run `python3 setup.py` for a configuration creator. If you don't do this, the bot will not run.
5. Before starting, make sure the Server Members Intent is enabled in your bot settings in the Discord Developer Portal.
6. To make sure the `mute` and `unmute` commands work, please make a role called `muted` in your server. The bot will not (yet) do this for you. After you create the role, make sure to create overrides for the channels you don't want a muted user speaking in.
7. Run the main bot file: `python3 start.py` (or see the commands with `python3 start.py --help`).

### Features

There are many features of the bot. These features include:

- VirusTotal file scanning
- Message encryption
- Moderation
- Fun commands
- Utility commands
- Custom playing status that you can customize per instance
- Self updating feature
- Lots more commands, and more commands being added regularly!

[![Join our Discord server!](https://invidget.switchblade.xyz/myzbqnVUFN)](http://discord.gg/myzbqnVUFN)

Like earlier said, if you have any feature requests or issues with the bot, open an issue [here](https://github.com/FOSS-Devs/freediscord/issues)!
Enjoy the bot! We hope you have as much fun with it as we had programming it! :)

Made with discord.py v9.
