# pylint: disable=missing-module-docstring, wildcard-import
import socket
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from configs import *

def connectFPT():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((FTP_SERVER, FTP_PORT))

    def runConvo(convo):
        res = []
        for c in convo:
            s.send(c.encode())
            response = s.recv(BUFFER).decode()

            print(response)
            res.append(response)

        return res

    # Receive the initial message from the server
    print(s.recv(1024).decode())

    runConvo([
        f'USER {USERNAME}\r\n',
        f'PASS {PASSWORD}\r\n',
        'LIST\r\n',
        'QUIT\r\n'
    ])

    # Close the socket
    s.close()


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