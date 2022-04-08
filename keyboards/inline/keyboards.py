import string

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import dir_callback, files_callback, drives_callback
import loader
from utils.misc.directoryTools import getDirFiles
from os.path import isdir, exists


def directInKb():
    kb = InlineKeyboardMarkup(row_width=3)
    kb.insert(InlineKeyboardButton('...', callback_data=dir_callback.new(id_directory=-1)))
    files = []

    for i in getDirFiles(loader.current_dir)[0]:
        try:
            getDirFiles(i)
        except PermissionError:
            continue
        except FileNotFoundError:
            continue

        files.append(i)

    for i in getDirFiles(loader.current_dir)[1]:
        files.append(loader.current_dir + i)

    for i in range(len(files)):
        if isdir(files[i]):
            kb.insert(InlineKeyboardButton(files[i][files[i].rfind('/', 0, -1) + 1:],
                                           callback_data=dir_callback.new(id_directory=i)))
        else:
            kb.insert(InlineKeyboardButton(files[i][files[i].rfind('/', 0, -1) + 1:],
                                           callback_data=files_callback.new(id_fileName=i)))

    return kb, files


def drivesInKb():
    available_drives = ['%s:' % d for d in string.ascii_uppercase if exists('%s:' % d)]
    kb = InlineKeyboardMarkup()

    for i in available_drives:
        i += '/'
        kb.insert(InlineKeyboardButton(i, callback_data=drives_callback.new(disk=i)))

    return kb
