from aiogram import Dispatcher

from loader import loop
from data.config import ADMINS
from utils.db_api.usersDB import shutdownAccess


async def shutdown(dp: Dispatcher):
    for admin in ADMINS:
        await dp.bot.send_message(admin, "The bot is disabled.")

    shutdownAccess()


