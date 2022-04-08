import logging
from datetime import datetime
import loader

from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.inline.callback_datas import dir_callback, files_callback, drives_callback
from keyboards.inline.keyboards import directInKb, drivesInKb

from loader import dp

from data.config import emailLogin, emailPassword, defaultEmail, ADMINS
from utils.misc.mailTools import send_email
from utils.db_api.usersDB import setAccess, getUser, shutdownAccess


@dp.message_handler(Command('clear'))
async def clear(msg: Message):
    if str(msg.from_user.id) in ADMINS:
        shutdownAccess()
        await msg.answer('All sessions except admins are completed')
    else:
        await msg.answer("You don't have permissions")


@dp.message_handler(Command('leave'))
async def leave(msg: Message):
    setAccess(msg.from_user.id, 0)
    await msg.answer('Leave successfully')


@dp.callback_query_handler(dir_callback.filter())
async def dirCall(call: CallbackQuery, callback_data: dict):
    if getUser(call.from_user.id)[2]:
        match int(callback_data.get('id_directory')):
            case -1:  # go back directory
                await call.answer()

                if loader.current_dir[:loader.current_dir.rfind('/', 0, -1) + 1]:
                    loader.current_dir = loader.current_dir[:loader.current_dir.rfind('/', 0, -1) + 1]
                    await call.message.edit_text(f'Current directory: {loader.current_dir}')
                    await call.message.edit_reply_markup(directInKb()[0])
                else:
                    await call.message.edit_text('Select the desired disk!')
                    await call.message.edit_reply_markup(drivesInKb())

            case _:
                await call.answer()
                loader.current_dir = directInKb()[1][int(callback_data.get('id_directory'))]
                await call.message.edit_text(f'Current directory: {loader.current_dir}')
                await call.message.edit_reply_markup(directInKb()[0])
    else:
        await call.message.edit_text('Access is denied. /login - to use the bot!')


@dp.callback_query_handler(files_callback.filter())
async def fileCall(call: CallbackQuery, callback_data: dict):
    if getUser(call.from_user.id)[2]:
        file_path = [directInKb()[1][int(callback_data.get('id_fileName'))]]
        now = datetime.now()
        time = "{}.{}.{}  {}:{}".format(str(now.day).rjust(2, '0'),
                                        str(now.month).rjust(2, '0'),
                                        now.year, str(now.hour).rjust(2, '0'),
                                        str(now.minute).rjust(2, '0'))
        logging.info(f'{file_path} ::: {time}')
        try:
            send_email(defaultEmail, f'Telegram bot {time}', '', file_path, (emailLogin, emailPassword))
            await call.message.answer(f"File {file_path} successfully send.")
        except:
            pass
        await call.answer()
    else:
        await call.message.edit_text('Access is denied. /login - to use the bot!')


@dp.callback_query_handler(drives_callback.filter())
async def changeDisk(call: CallbackQuery, callback_data: dict):
    if getUser(call.from_user.id)[2]:
        loader.current_dir = callback_data.get('disk')
        await call.message.edit_text(f'Current dir: {loader.current_dir}')
        await call.message.edit_reply_markup(directInKb()[0])
        await call.answer()
    else:
        await call.message.edit_text('Access is denied. /login - to use the bot!')
