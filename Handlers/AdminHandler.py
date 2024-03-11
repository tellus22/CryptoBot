from aiogram import types
from aiogram.filters import Command

from Database.MyDb import get_all_users
from config import ADMIN_CHAT_ID
from loader import dp, bot


@dp.message(Command('get_all'))
async def get_all_users_command(message: types.Message):
    if message.from_user.id == ADMIN_CHAT_ID:
        await get_all_users(message)


async def admin_message():
    await bot.send_message(ADMIN_CHAT_ID, "Бот запущен")
