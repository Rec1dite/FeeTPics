# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring
import os
import shutil
import argparse
import binascii
import datetime
import json
from configs import *
from socks import sendFile, listFiles
from pics import patchFolder
from feet import observe

# Gets the initial project configuration if it exists, else creates it
def initFeetpics(projId = None):
    config = {}
    if os.path.isdir(".feetpics"):
        # Project already initialized
        # Read config

        with open(".feetpics/config", "r", encoding='utf-8') as f:
            config = json.loads(f.read())

    else:
        # Project not initialized
        os.mkdir(".feetpics")
        os.mkdir(".feetpics/temp") # Workspace where we construct new backups
        os.mkdir(".feetpics/backups") # Stores the latest backup zips

        # Create .feetpics/confilive shareg
        config = {
            "name": "/".join(cwd.split(os.sep)[:-2]),
            "id": binascii.b2a_hex(os.urandom(16)).decode("utf-8") if projId == None else projId,
            "created": datetime.datetime.now().timestamp(),
            "backupInterval": 60, # The min time between backups in seconds
            "lastBackup": 0, # Unix timestamp of the last backup
        }

        with open(".feetpics/config", "w", encoding='utf-8') as f:
            f.write(json.dumps(config))

    return config

def writeConfig(config):
    with open(".feetpics/config", "w", encoding='utf-8') as f:
        f.write(json.dumps(config))

def runInteractive(config):
    running = True

    while running:
        command = input("Enter a command: ").split()

        match command[0]:
            case "help":
                print("help\t\t\t- Display this help message")
                print("list\t\t\t- List all backups")
                print("backup\t\t\t- Backup the current directory")
                print("restore <timestamp>\t- Restore from the specified backup")
                print("nuke\t\t\t- Delete all backups")

            case "list":
                print("Backups as of " + C_BLUE + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + C_RESET + ":")

            case "backup":
                print("Backing up...")
            
            case "restore":
                if len(command) > 1:
                    if command[1].isnumeric():
                        print("Restoring...")
            
            case "nuke":
                confirm = input("Are you sure you want to delete all backups? (y/N): ")
                match confirm:
                    case "y" | "Y":
                        print("Nuking...")
                    case "n" | "N" | "":
                        print("Aborting nuke")
            
            case "exit" | "quit":
                running = False

def runObserver(config):
    # Detect file changes
    # Check if config["backupInterval"] time has elapsed since last backup
    pass

if __name__ == '__main__':
    cwd = os.getcwd()
    config = initFeetpics()

    patchFolder("./.feetpics/latest", ".", ".feetpics/temp")

    #===== CHECK LATEST BACKUP =====#
    # Update .feetpics/latest with the latest backup (this allows us to perform diffs)
    ftp_files = listFiles(f"/feetpics/{config['id']}")

    if ftp_files["status"] != "success":
        # Create backup directory
        pass


    #===== CHECK ARGUMENTS =====#
    parser = argparse.ArgumentParser(
        prog="feetpics",
        description="A simple FTP backup tool"
        )

    parser.add_argument("-i", "--interactive", action="store_true", help="run in interactive mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="print verbose output")
    args = parser.parse_args()

    if args.interactive:
        runInteractive(config)

    else:
        runObserver(config)
    #===== START OBSERVER =====#

    # sendFile("./test.txt", "/test/asdf/fdsa")