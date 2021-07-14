# Copyright (c) 2021 SKBotNL (and the members of the FOSS-Devs)
# See LICENSE in the project root for license information.

import os
print("Welcome to the FOSSDiscord interactive setup script!")
def tokenWrite() :
    writeBotToken = input("Enter your bot token: ")
    verificationOne = input("Is this correct? (y/n): '" + writeBotToken + "'")
    if verificationOne == "y":
        print("Writing...")
        writeTokenTemplate = "bot_token = '" + writeBotToken + "'\n"
        config = open('config.py', 'a')
        config.write(writeTokenTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationOne == "n":
        print("Please rerun the file and input the correct bot token.")
        exit()
    elif verificationOne != "n" or "y":
        print("Invalid response, please rerun the script.")
        exit()

def prefixWrite() :
    writePrefix = input("Enter the bot's prefix: ")
    verificationTwo = input("Is this correct? (y/n): '" + writePrefix + "'")
    if verificationTwo == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "prefix = '" + writePrefix + "'\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!\n")
        #print(writeTokenTemplate)
    elif verificationTwo == "n":
        print("Please rerun the file and input your preferred bot prefix.")
        exit()
    elif verificationTwo != "n" or "y":
        print("Invalid response, please rerun the script.")
        exit()

def ownerIDWrite() :
    ownerIDinput = input("Enter the bot owner's user ID: ")
    verificationThree = input("Is this correct? (y/n): '" + ownerIDinput + "'")
    if verificationThree == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "ownerID = '" + ownerIDinput + "'\n"
        config.write(writePrefixTemplate)
        config.close()
        config = open('config.py', 'r')
    elif verificationThree == "n":
        print("Please rerun the file and input the bot owner's user ID")
        exit()
    elif verificationThree != "n" or "y":
        print("Invalid response, please rerun the script.")
        exit()

def vtapiWrite() :
    print("If you don't have a VirusTotal API key (get one here https://virustotal.com), or don't want this feature, just hit enter on this prompt and type 's' when it asks if what you inputted is correct.\n")
    vtapiToken = input("Enter your VirusTotal API key: ")
    verificationFour = input("Is this correct? (y/n/s): '" + vtapiToken + "'")
    if verificationFour == "y":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "virustotal_api = '" + vtapiToken + "'\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationFour == "n":
        print("Please rerun the file and input your VirusTotal API key.")
        exit()
    elif verificationFour == "s":
        print("Writing...")
        config = open('config.py', 'a')
        writePrefixTemplate = "virustotal_api = ''\n"
        config.write(writePrefixTemplate)
        config.close()
        print("Written!")
        print()
        print("You have chosen not to input a VirusTotal API key. You may add one by editing the config.py file later.")
    elif verificationFour != "n" or "y" or "s":
        print("Invalid response, please rerun the script.")
        exit()

def dateformatWrite() :
    print("Please choose the default date format that will be used in the messages.")
    print("Choices: 1) day/month/year hour:minutes AM/PM 2) month/day/year hour:minutes AM/PM 3) day/month/year hour:minutes (24 hour) 4) month/day/year hour:minutes (24 hour)")
    writedateformat = input("Enter the number of your choice: ")
    verificationOne = input("Is this correct? (y/n): '" + writedateformat + "'")
    if verificationOne == "y":
        print("Writing...")
        if writedateformat == "1":
            writeDateFormatTemplate = "date_format = '%d/%m/%Y, %I:%M %p'\n"
        elif writedateformat == "2":
            writeDateFormatTemplate = "date_format = '%m/%d/%Y, %I:%M %p'\n"
        elif writedateformat == "3":
            writeDateFormatTemplate = "date_format = '%d/%m/%Y, %H:%M'\n"
        elif writedateformat == "4": 
            writeDateFormatTemplate = "date_format = '%m/%d/%Y, %H:%M'\n"
        else:
            print("Invalid response, please rerun the script.")
        config = open('config.py', 'a')
        config.write(writeDateFormatTemplate)
        config.close()
        print("Written!")
        print()
    elif verificationOne == "n":
        print("Please rerun the file and input the correct number.")
        exit()
    elif verificationOne != "n" or "y":
        print("Invalid response, please rerun the script.")
        exit()

if os.path.exists("config.py"):
    prompt = input("Existing config.py found. Should I delete it? (y/n)")
    if prompt == "y":
        print("Deleting existing config file...")
        os.remove("config.py")
        print("Deleted! Continuing with normal script now...")
        print()
    elif prompt == "n":
        print("Exiting...")
        exit()
    elif prompt != "n" or "y":
        print("Invalid response, please rerun the script.")
        exit()

tokenWrite()
prefixWrite()
ownerIDWrite()
vtapiWrite()
dateformatWrite()

print("Your config file should be written now!")
print("To start your bot, run 'python (or python3) bot.py'")
print("Have a nice day! :)")
exit()