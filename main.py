# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring
import time
from ftp import sendFile
from ftp import deleteFile
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileSystemEvent
from watchdog.events import FileSystemMovedEvent
from watchdog.observers import Observer
from configs import *


class UpdateEventHandler(FileSystemEventHandler):
    def on_created(self, event:FileSystemEvent):
        sendFile(event.src_path)

    def on_moved(self, event:FileSystemMovedEvent):
        # This is very bad code you are supposed to use the Rename From(RNFR) followed by Rename to (RNTO) command.
        sendFile(event.dest_path)
        deleteFile(event.src_path)

    def on_deleted(self, event:FileSystemEvent):
        deleteFile(event.src_path)

    def on_modified(self, event:FileSystemEvent):
        sendFile(event.src_path)

if __name__ == '__main__':

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