# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring
from socks import sendFile, listFiles
from feet import observe

if __name__ == '__main__':
    sendFile("./test.txt")
    listFiles()