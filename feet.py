# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring

import os
import time
import json
from watchdog.events import FileSystemEventHandler
from watchdog.events import DirModifiedEvent
from watchdog.observers import Observer
from socks import sendFile
from pics import makeBackupArchive, patchFolder
from configs import *

def writeConfig(config):
    with open(".feetpics/config", "w", encoding='utf-8') as f:
        f.write(json.dumps(config))

def handleEvent(event, config, message="changed", verbose=False):
    # TODO: Check properly if this is the .feetpics folder
    if ".feetpics" in event.src_path:
        return

    print(C_ORANGE + f"File {message}: " + C_RESET + event.src_path)

    # Check if sufficient time has passed since the last backup
    if config["lastBackup"] + config["backupInterval"] <= time.time():
        print(C_GREEN + "Timer passed, backing up" + C_RESET)

        backupTime = int(time.time())
        config["lastBackup"] = backupTime
        writeConfig(config)

        #===== Create backup =====#

        # Create patches in .feetpics/temp
        patchFolder("./.feetpics/latest", ".", ".feetpics/temp")

        # Zip patches into .feetpics/backups
        makeBackupArchive(backupTime)

        # Send the backup .zip to the server
        sendFile(f"./.feetpics/backups/{backupTime}.zip", f"/feetpics/{config['id']}/{backupTime}.zip")

class UpdateEventHandler(FileSystemEventHandler):
    config = {}
    verbose = False

    def on_created(self, event):
        handleEvent(event, self.config, "created", self.verbose)

    def on_moved(self, event):
        handleEvent(event, self.config, "moved", self.verbose)

    def on_deleted(self, event):
        handleEvent(event, self.config, "deleted", self.verbose)

    def on_modified(self, event):
        # Ignore directory modifications
        if (isinstance(event, DirModifiedEvent)):
            return

        handleEvent(event, self.config, "modified", self.verbose)

def observe(path, config, verbose=False):
    observer = Observer()

    eventHandler = UpdateEventHandler()
    eventHandler.config = config
    eventHandler.verbose = verbose

    observer.schedule(event_handler=eventHandler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()