# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring

import os
import json
from time import time
from watchdog.events import FileSystemEventHandler
from watchdog.events import DirModifiedEvent
from watchdog.observers import Observer
from socks import sendFile
from configs import PATH

def checkfile() -> bool:
    path = './.feetpics/backups'
    # iterate over files in the directory
    backup = ""
    for filename in os.listdir(path):
        # check if the file is a regular file (i.e. not a directory)
        if os.path.isfile(os.path.join(path, filename)):
            # print the name of the file
            backup = filename.split(".")[0]
    if backup == "":
        return True
    with open('./.feetpics/config', 'r', encoding="utf-8") as f:
        json_data = f.read()
    
    # parse the JSON data and convert it to a dictionary
    timer = int (json.loads(json_data)["backupInterval"])
    print(timer)
    print(str(int(time.time()))  + ">=" + str(timer + int(backup)))
    if (int(time.time())  >= (timer + int(backup))):
        os.remove(f'./.feetpics/backups/{backup}.zip')
        return True
    return False

def sendArchive():
    path = './.feetpics/backups'
    # iterate over files in the directory
    backup = ""
    for filename in os.listdir(path):
        # check if the file is a regular file (i.e. not a directory)
        if os.path.isfile(os.path.join(path, filename)):
            # print the name of the file
            backup = filename

    sendFile(f"./.feetpics/backups/{backup}",backup)
class UpdateEventHandler(FileSystemEventHandler):

    def on_created(self, event):
        if (checkfile()):
            makeArchive(PATH)
            sendArchive()

    def on_moved(self, event):
        if (checkfile()):
            makeArchive(PATH)
            sendArchive()

    def on_deleted(self, event):
        if (checkfile()):
            makeArchive(PATH)
            sendArchive()

    def on_modified(self, event):
        if (isinstance(event, DirModifiedEvent)):
            return
        if (checkfile()):
            makeArchive(PATH)
            sendArchive()

# TODO: We might want to expose callbacks to the above
#       functions through parameters in observe(...)
def observe(path):
    observer = Observer()
    eventHandler = UpdateEventHandler()
    observer.schedule(event_handler=eventHandler, path=path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()