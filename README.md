# FeeTPics

A simple Python FTP client to backup your files as they are modified.

## Project structure
- `socks.py` -> "sockets", where we do all the FTP connection/communication
- `feet.py` -> "deployed on the ground", utilities to listen for changes in the filesystem
- `pics.py` -> "snapshotting" system, computes file diffs and performs patches, as well as bundling files into archives