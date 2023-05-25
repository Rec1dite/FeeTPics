# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring

import socket
import random
from configs import *

#========== UTILITY FUNCTIONS ==========#

# Connect to the FTP server & authenticate
def connectCtrl(verbose = False):
    #===== CONNECT CONTROL PORT =====#
    ctrlSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ctrlSock.connect((FTP_SERVER, FTP_CTRL_PORT))

    # Receive the initial message from the server
    if verbose:
        print(ctrlSock.recv(1024).decode())

    # Authenticate
    runConvo(ctrlSock, [
        f'USER {USERNAME}\r\n',
        f'PASS {PASSWORD}\r\n',
    ], verbose=verbose)

    return ctrlSock

# Establish a data connection with the server
def connectData(ctrlSock, verbose = False):

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
    ], verbose=verbose)

    return dataSock

# Throw a bunch of FTP commands at the server
def runConvo(sock, convo, verbose = False):
    res = []
    for c in convo:
        sock.send(c.encode())
        response = sock.recv(BUFFER).decode()

        if verbose:
            print(c, end="")
            print(C_ORANGE + response + C_RESET)

        res.append(response)

    return res


#========== FTP FUNCTIONS ==========#
# Returns a list of filenames in the specified FTP directory
def listFiles(ftpDir="/", verbose = False):
    ctrlSock = connectCtrl(verbose=verbose)
    dataSock = connectData(ctrlSock, verbose=verbose)

    # Get files on server
    resp = runConvo(ctrlSock, [ f'CWD {ftpDir}\r\n', ], verbose=verbose)

    if resp[0].startswith('550'):
        if verbose:
            print(C_RED + 'Failed to open folder' + C_RESET)
        return { "status": "failed", "data": []}

    runConvo(ctrlSock, [ 'LIST\r\n' ], verbose=verbose)

    conn, _ = dataSock.accept()

    files = ""
    while True:
        data = conn.recv(BUFFER).decode()
        files += data

        if not data: break

    def extractFilename(s):
        parts = s.split(maxsplit=8)
        filename = parts[-1]
        return filename

    res = []
    for f in files.split('\r\n'):
        if f:
            res.append(extractFilename(f))

    # Close connections
    conn.close()
    dataSock.close()

    runConvo(ctrlSock, [ 'QUIT\r\n' ])
    ctrlSock.close()

    return { "status": "success", "data": res }

# Send file at `path` over FTP and store as `name`
def makeDir(ftpPath, verbose = False):
    ctrlSock = connectCtrl()

    # This will prompt the server to immediately connect to our data socket
    runConvo(ctrlSock, [ f'MKD {ftpPath}\r\n' ], verbose=verbose)

    runConvo(ctrlSock, [ 'QUIT\r\n' ], verbose=verbose)
    ctrlSock.close()

# Send file at `path` over FTP and store as `name`
def sendFile(path, name, verbose = False):
    ctrlSock = connectCtrl()
    dataSock = connectData(ctrlSock)

    # This will prompt the server to immediately connect to our data socket
    runConvo(ctrlSock, [ f'STOR {name}\r\n' ])

    conn, _ = dataSock.accept() # Embrace connection 🤗

    # Send file
    with open(path, 'rb') as file:
        conn.send(file.read())


    # Close connections
    conn.close() # Tells the server we're done sending data
    dataSock.close()

    runConvo(ctrlSock, [ 'QUIT\r\n' ])
    ctrlSock.close()