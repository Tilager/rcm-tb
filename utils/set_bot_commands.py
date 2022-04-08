from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start bot"),
            types.BotCommand("login", "Login session"),
            types.BotCommand("help", "Get help"),
            types.BotCommand("leave", "Log out"),
        ]
    )
