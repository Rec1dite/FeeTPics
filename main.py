# pylint: disable=missing-module-docstring, wildcard-import
import socket
from configs import *

def connectFPT():
    # Connect
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

if __name__ == '__main__':
    connectFPT()