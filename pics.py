# pylint: disable=missing-module-docstring, wildcard-import, unused-wildcard-import, missing-function-docstring, invalid-name, missing-class-docstring
import os
import time
from shutil import make_archive
from diff_match_patch import diff_match_patch
from configs import *

dmp = diff_match_patch()

# Package all files in temp folder into a zip archive and save in backups folder
def makeBackupArchive(archiveName):
    make_archive(f'./.feetpics/backups/{archiveName}', 'zip', './.feetpics/temp')

def cleanPatches():
    for subdir, _, files in os.walk("./.feetpics/temp"):
        for file in files:
            if file.endswith(".patch"):
                os.remove(os.path.join(subdir, file))

# Descend through subdirectories of a folder and create a patch for each file
def patchFolder(folderAfter, outFolder):
    for subdir, _, files in os.walk(folderAfter):

        # Skip dotfiles
        if True in map(lambda s: s.startswith('.') or s.startswith('__'), subdir.split('/')[1:]):
            continue

        for file in files:
            if not file.startswith('.'):
                beforePath = os.path.join("./.feetpics/latest", subdir[1:], file)
                afterPath = os.path.join(subdir, file)

                if os.path.isfile(afterPath):
                    createFilePatch(beforePath, afterPath, f'./{outFolder}/{file}.patch')

def createFilePatch(fileBefore, fileAfter, outFile):
    txtBefore = ""
    txtAfter = ""

    # if fileBefore does not exist, create an empty file
    if not os.path.isfile(fileBefore):
        with open(fileBefore, "w", encoding='utf-8') as f:
            f.write("")

    with open(fileBefore, "r", encoding='utf-8') as f:
        txtBefore = f.read()

    with open(fileAfter, "r", encoding='utf-8') as f:
        txtAfter = f.read()

    patch = dmp.patch_make(txtBefore, txtAfter)

    # Skip patching if no changes
    if len(patch) == 0:
        return

    print(f"{C_BLUE}Patching {fileAfter}{C_RESET}")

    # If folder doesn't exist, create it
    if not os.path.exists(os.path.dirname(outFile)):
        os.makedirs(os.path.dirname(outFile))

    with open(outFile, "w", encoding='utf-8') as f:
        f.write(dmp.patch_toText(patch))

    # Save the latest version of the file
    with open(fileBefore, "w", encoding='utf-8') as f:
        f.write(txtAfter)