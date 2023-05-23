# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring
import os
import time
from shutil import make_archive
from diff_match_patch import diff_match_patch
from configs import *

dmp = diff_match_patch()

def makeArchive(folderToZip)->str:
    curtime = str(int(time.time()))
    archive = make_archive(f'./.feetpics/backups/{curtime}', 'zip', f'{folderToZip}')


# Descend through subdirectories of a folder and create a patch for each file
def patchFolder(folderBefore, folderAfter, outFolder):
    for subdir, dirs, files in os.walk(folderAfter):

        # Skip dotfiles
        if True in map(lambda s: s.startswith('.'), subdir.split('/')[1:]):
            continue

        for file in files:
            if not file.startswith('.'):
                beforePath = os.path.join(folderBefore, subdir, file)
                afterPath = os.path.join(subdir, file)

                print(beforePath)
                print(afterPath)
                print()

                if os.path.isfile(beforePath):
                    pass
                    createFilePatch(beforePath, afterPath, f'{outFolder}/{file}.patch')

def createFilePatch(fileBefore, fileAfter, outFile):
    txtBefore = ""
    txtAfter = ""

    with open(fileBefore, "r", encoding='utf-8') as f:
        txtBefore = f.read()

    with open(fileAfter, "r", encoding='utf-8') as f:
        txtBefore = f.read()

    patch = dmp.patch_make(txtBefore, txtAfter)

    # If folder doesn't exist, create it
    if not os.path.exists(os.path.dirname(outFile)):
        os.makedirs(os.path.dirname(outFile))

    with open(outFile, "w", encoding='utf-8') as f:
        f.write(dmp.patch_toText(patch))

    # dmp.patch_toText(patch)