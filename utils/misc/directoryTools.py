import os


def getDirFiles(directory: str):
    files = []
    dirs = []
    for i in os.listdir(directory):
        if os.path.isdir(directory + i):
            dirs.append(directory + i + '/')
        else:
            files.append(i)
    return dirs, files