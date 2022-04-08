from aiogram import types
from aiogram.dispatcher import FSMContext

import loader
from keyboards.inline.keyboards import directInKb
from loader import dp, current_dir

from utils.db_api.usersDB import addUser, getUser, setCode, setAccess
from utils.misc.mailTools import send_code_confirmation
from data.config import emailLogin, emailPassword, defaultEmail

from states.confirmation_codes import ConfCode


@dp.message_handler(commands=['start', 'login'])
async def bot_start(msg: types.Message):
    addUser(msg.from_user.id, msg.from_user.username, False)

    if getUser(msg.from_user.id)[2]:  # access is allowed
        await msg.answer(f'Current directory: {current_dir}', reply_markup=directInKb()[0])
    else:  # access is denied
        await msg.answer(f"Access is denied. Enter the confirmation code:")
        setCode(msg.from_user.id,
                send_code_confirmation(defaultEmail, (emailLogin, emailPassword))
                )
        await ConfCode.S1.set()


@dp.message_handler(state=ConfCode.S1)
async def waitCode(msg: types.Message, state: FSMContext):
    code = msg.text
    if code == getUser(msg.from_user.id)[3]:
        setAccess(msg.from_user.id, 1)
        await msg.answer(f'Current directory: {loader.current_dir}',
                         reply_markup=directInKb()[0])
        await state.finish()
    else:
        await msg.answer('Invalid code. Try again:')
        await ConfCode.S1.set()
