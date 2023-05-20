# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring

import socket
import os
from configs import *

# Set up some constants
FILE_PATH = 'path/to/your/file'

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
    # runConvo(ctrlSock, [ 'LIST\r\n' ])

    #===== CONNECT DATA PORT =====#
    filename = FILE_PATH.rsplit(os.sep, maxsplit=1)[-1]

    resp = runConvo(ctrlSock, [
        'TYPE I\r\n', # Enter binary mode
        f'STOR {filename}\r\n', # Send the STOR command
    ])

    if resp[-1][0] != '1':
        print(C_RED + "❌ Error:", resp[-1] + C_RESET, end="")
        print(C_RED + "| Check that you have write permissions on the server bozo" + C_RESET)
        return

    dataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataSock.connect((FTP_SERVER, FTP_DATA_PORT))

    #===== SEND FILE =====#

    # Open the file and send its contents
    with open(FILE_PATH, 'rb') as file:
        dataSock.send(file.read())

    #===== CHECK FILE CORRECTLY RECEIVED =====#
    # TODO
    resp = dataSock.recv(BUFFER).decode()
    # print(resp) # Hopefully 226 Transfer complete 🤞

    runConvo(dataSock, [ 'QUIT\r\n' ])
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