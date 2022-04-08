from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Command list: ",
            "/start - Login session or start bot",
            "/login - Login session or start bot",
            "/clear - Log out of all sessions (Command for admin)",
            "/leave - Log out",
            "/exit - Bot stop (Command for admin)",
            "/help - Get help")
    
    await message.answer("\n".join(text))
