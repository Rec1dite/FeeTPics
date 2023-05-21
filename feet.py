# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring

from time import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from socks import sendData

class UpdateEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        conversation = [ f'STOR {filename}\r\n' ]
        sendData(path=event.src_path,write=True,conversation=conversation)
        pass

    def on_moved(self, event):
        pass

    def on_deleted(self, event):
        conversation = [ f'DELE {filename}\r\n' ]
        sendData(path=event.src_path,conversation=conversation)
        pass

    def on_modified(self, event):
        conversation = [ f'STOR {filename}\r\n' ]
        sendData(path=event.src_path,write=True,conversation=conversation)
        pass

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