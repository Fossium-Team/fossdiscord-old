import os, ctypes, sys, subprocess, config

commands = ["--help", "--updatebot", "--start", "--credits"]

def startbot():
    print("Attempting to start the bot...")
    print("REMEMBER: YOU MUST RUN THE COMMAND '" + config.prefix + "shutdownbot' TO SHUTDOWN THE BOT!!!!")
    dir_path = os.getcwd()
    subprocess.Popen(['python', dir_path + '/bot.py'])
    sys.exit()

def botupdate():
    if sys.platform == "linux" or sys.platform == "linux2":
        try:
            os.mkdir('/tmp/freeupdate')
        except OSError:
            os.rmdir('/tmp/freeupdate')
            os.mkdir('/tmp/freeupdate')
        HTTPS_REMOTE_URL = globalconfig.github_login_url
        DEST_NAME = '/tmp/freeupdate'
        cloned_repo = Repo.clone_from(HTTPS_REMOTE_URL, DEST_NAME)
        dir_path = os.getcwd()
        shutil.rmtree(dir_path + "/cogs/")
        path = dir_path
        src = '/tmp/freeupdate/cogs'
        dest = dir_path + "/cogs"
        destination = shutil.copytree(src, dest)
        copyfile('/tmp/freeupdate/bot.py', dir_path + '/bot.py')
        copyfile('/tmp/freeupdate/setup.py', dir_path + '/setup.py')
        copyfile('/tmp/freeupdate/README.md', dir_path + '/README.md')
        copyfile('/tmp/freeupdate/globalconfig.py', dir_path + '/globalconfig.py')
        shutil.rmtree('/tmp/freeupdate')
        print("Done! Restart the bot to apply the changes!")
        print(title = "Updated!", description = "FreeDiscord updated! No error reported. Check your console to confirm this.")
    elif sys.platform == "win32":
        print("'updatebot' is not yet available for Windows.")
    elif sys.platform == "darwin":
        print("'updatebot' is not yet available for macOS.")

try:
    booloutput = bool(sys.argv[1])
except:
    startbot()
for commandList in commands:
    if sys.argv[1] not in commands:
        sys.exit(sys.argv[1] + " is not a command. To get a command list, run 'python3 start.py --help'.")

if "--help" in sys.argv[1]:
    try:
        bool(sys.argv[2])
    except:
        sys.exit("FreeDiscord Start Script\nCommand List:\n\t--help - This message\n\t--start (or no argument) - Starts this FreeDiscord instance.\n\t--credits - Shows the credits of FreeDiscord.\n\t--updatebot - Updates this FreeDiscord instance.")
    if sys.argv[2] == "gui":
        sys.exit("FreeDiscord Start Script\npython3 start.py --start\nStarts the bot.")
    elif sys.argv[2] == "help":
        sys.exit("FreeDiscord Start Script\npython3 start.py --help\nShows the command list.")
    elif sys.argv[2] == "crash":
        sys.exit("FreeDiscord Start Script\npython3 start.py --updatebot\nUpdates the FreeDiscord instance.")
    elif sys.argv[2] == "credits":
        sys.exit("redev's CrashDash\npython3 start.py --credits\nShows the credits of FreeDiscord.")

if "--updatebot" in sys.argv[1]:
    botupdate()

if "--start" in sys.argv[1]:
    startbot()
