# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring
import time
from ftp import sendFile
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from configs import *


class UpdateEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        connectFPT()

    def on_moved(self, event):
        connectFPT()

    def on_deleted(self, event):
        connectFPT()

    def on_modified(self, event):
        connectFPT()

if __name__ == '__main__':

    sendFile("./test.txt")
    exit()

    observer = Observer()
    eventHandler = UpdateEventHandler()
    observer.schedule(event_handler=eventHandler,path=PATH,recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()