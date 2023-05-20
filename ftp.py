# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring

import socket
import random
import os
from configs import *

def sendFile(path):

    #===== CONNECT CONTROL PORT =====#
    ctrlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrlSock.connect((FTP_SERVER, FTP_CTRL_PORT))

    def runConvo(sock, convo):
        res = []
        for c in convo:
            sock.send(c.encode())
            response = sock.recv(BUFFER).decode()

            print(c)
            print(C_ORANGE + response + C_RESET)

            res.append(response)

        return res

    # Receive the initial message from the server
    print(ctrlSock.recv(1024).decode())

    # Authenticate
    runConvo(ctrlSock, [
        f'USER {USERNAME}\r\n',
        f'PASS {PASSWORD}\r\n',
    ])

    # Get files on server
    # runConvo(ctrlSock, [
    #     'LIST\r\n',
    #     'PWD\r\n',
    #     'QUIT\r\n'
    #     ])
    # ctrlSock.close()
    # exit()

    #===== CONNECT DATA PORT =====#
    # Establish filename to save in the FTP directory
    filename = path.rsplit(os.sep, maxsplit=1)[-1]
    filename = "test.txt"

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
        # 'PASV\r\n',
        # Enter binary mode
        'TYPE I\r\n',
        # Tell the server what ip/port to connect to
        f'PORT {portArgs}\r\n',
    ])

    # This will prompt the server to connect to our data socket
    runConvo(ctrlSock, [ f'STOR {filename}\r\n' ])

    conn, addr = dataSock.accept() # Embrace connection 😳
    print(f"{C_GREEN}CONNECTED {C_RED}{addr}{C_RESET}")

    #===== SEND FILE =====#
    with open("./test.txt", 'rb') as file:
        conn.send(file.read())

    conn.close() # Tells the server we're done sending data
    dataSock.close()

    runConvo(ctrlSock, [ 'QUIT\r\n' ])
    ctrlSock.close()


def deleteFile(path):

    #===== CONNECT CONTROL PORT =====#
    ctrlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrlSock.connect((FTP_SERVER, FTP_CTRL_PORT))

    def runConvo(sock, convo):
        res = []
        for c in convo:
            sock.send(c.encode())
            response = sock.recv(BUFFER).decode()

            print(c)
            print(C_ORANGE + response + C_RESET)

            res.append(response)

        return res

    # Receive the initial message from the server
    print(ctrlSock.recv(1024).decode())

    # Authenticate
    runConvo(ctrlSock, [
        f'USER {USERNAME}\r\n',
        f'PASS {PASSWORD}\r\n',
    ])

    # Get files on server
    # runConvo(ctrlSock, [ 'LIST\r\n' ])

    #===== CONNECT DATA PORT =====#
    filename = FILE_PATH.rsplit(os.sep, maxsplit=1)[-1]

    resp = runConvo(ctrlSock, [
        'TYPE I\r\n', # Enter binary mode
        f'DELE {filename}\r\n', # Send the DELE command
    ])

    if resp[-1][0] != '1':
        print(C_RED + "❌ Error:", resp[-1] + C_RESET, end="")
        print(C_RED + "| Check that you have write permissions on the server bozo" + C_RESET)
        return

    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataSock.connect((FTP_SERVER, FTP_DATA_PORT))

    #===== CHECK FILE CORRECTLY RECEIVED =====#
    # TODO
    resp = dataSock.recv(BUFFER).decode()
    # print(resp) # Hopefully 226 Transfer complete 🤞

    runConvo(dataSock, [ 'QUIT\r\n' ])
    dataSock.close()
    runConvo(ctrlSock, [ 'QUIT\r\n' ])
    ctrlSock.close()