# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring

from time import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class UpdateEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        pass

    def on_moved(self, event):
        pass

    def on_deleted(self, event):
        pass

    def on_modified(self, event):
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