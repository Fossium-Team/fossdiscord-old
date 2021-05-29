# FreeDiscord
## Welcome to the official GitHub page of the FreeDiscord bot!
FreeDiscord is a Discord bot made by the reoccurdevs team ([ItsJustLag](https://github.com/ItsJustLag), [reoccurcat](https://github.com/reoccurcat), [Odysseus](https://github.com/Odysseus443), and [antistalker](https://github.com/stalker0000)) that you can edit and self host. This bot is 100% open source, so feel free to make forks of it, if you want. Just *please* at least give the original product some credit, and don't say you created the bot yourself. We appreciate it. :)
If you find an issue, or have a feature suggestion, please let us know by opening an issue [here](https://github.com/reoccurdevs/freediscord/issues).

## Documentation

### Starting the bot
#### Make sure you have [Python 3](https://www.python.org/downloads/) installed (and put in path, if you're on Windows 10)!!!
1. Clone the repository: `git clone https://github.com/reoccurdevs/freediscord.git` and go to step 2. An alternative is to download the ZIP file, unzip it, shift + right click in the `freediscord-main` folder, click on `Open Powershell window here`, and continue with step 3.
2. `cd` to the repository folder: `cd freediscord`.
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

Like earlier said, if you have any feature requests or issues with the bot, open an issue [here](https://github.com/reoccurdevs/freediscord/issues)!
Enjoy the bot! We hope you have as much fun with it as we had programming it! :)

Made with discord.py v9.
