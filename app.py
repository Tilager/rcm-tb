from aiogram.utils import executor

from loader import dp, loop

import middlewares, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from utils.shutdown import shutdown


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    # Startup notify
    await on_startup_notify(dispatcher)


async def on_shutdown(dispatcher):
    # Stop bot
    await shutdown(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, loop=loop, on_shutdown=on_shutdown)
