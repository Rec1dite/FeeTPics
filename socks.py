# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring

import socket
import random
import os
from configs import *

#========== UTILITY FUNCTIONS ==========#

# Connect to the FTP server & authenticate
def connectCtrl():
    #===== CONNECT CONTROL PORT =====#
    ctrlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrlSock.connect((FTP_SERVER, FTP_CTRL_PORT))

    # Receive the initial message from the server
    print(ctrlSock.recv(1024).decode())

    # Authenticate
    runConvo(ctrlSock, [
        f'USER {USERNAME}\r\n',
        f'PASS {PASSWORD}\r\n',
    ])

    return ctrlSock

# Establish a data connection with the server
def connectData(ctrlSock):

    # Create a new socket for the server to connect back to
    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CLIENT_PORT = 10000 + random.randint(0, 10000)

    # Find an open port
    foundOpenPort = False
    while not foundOpenPort:
        try:
            dataSock.bind(("", CLIENT_PORT))
            foundOpenPort = True
        except OSError:
            CLIENT_PORT = 10000 + random.randint(0, 10000)

    dataSock.listen(1)

    # Get our IP address
    CLIENT_HOST = socket.gethostbyname(socket.gethostname())
    CLIENT_HOST = ','.join(CLIENT_HOST.split('.'))

    portArgs = CLIENT_HOST + ',' + str(CLIENT_PORT // 256) + ',' + str(CLIENT_PORT % 256)

    runConvo(ctrlSock, [
        # Enter binary mode
        'TYPE I\r\n',
        # Tell the server what ip/port to connect to
        f'PORT {portArgs}\r\n',
    ])

    return dataSock

# Throw a bunch of FTP commands at the server
def runConvo(sock, convo):
    res = []
    for c in convo:
        sock.send(c.encode())
        response = sock.recv(BUFFER).decode()

        print(c, end="")
        print(C_ORANGE + response + C_RESET)

        res.append(response)

    return res


#========== FTP FUNCTIONS ==========#
def listFiles():
    ctrlSock = connectCtrl()
    dataSock = connectData(ctrlSock)

    # Get files on server
    runConvo(ctrlSock, [ 'LIST\r\n' ])
    conn, addr = dataSock.accept()

    # Print files
    print(conn.recv(BUFFER).decode())

    # Close connections
    conn.close()
    dataSock.close()

    runConvo(ctrlSock, [ 'QUIT\r\n' ])
    ctrlSock.close()

def sendFile(path):
    ctrlSock = connectCtrl()
    dataSock = connectData(ctrlSock)

    # Establish filename to save in the FTP directory
    filename = path.rsplit(os.sep, maxsplit=1)[-1]
    filename = "test.txt"

    # This will prompt the server to immediately connect to our data socket
    runConvo(ctrlSock, [ f'STOR {filename}\r\n' ])

    conn, addr = dataSock.accept() # Embrace connection 🤗
    # print(f"{C_GREEN}CONNECTED {C_RED}{addr}{C_RESET}")

    # Send file
    with open("./test.txt", 'rb') as file:
        conn.send(file.read())


    # Close connections
    conn.close() # Tells the server we're done sending data
    dataSock.close()

    runConvo(ctrlSock, [ 'QUIT\r\n' ])
    ctrlSock.close()