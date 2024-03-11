import sqlite3 as sq

from aiogram import types
from aiogram.enums import ParseMode


async def db_start():
    global db, cursor
    db = sq.connect('crypto.db')
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS profile("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                   "user_id INTEGER, "
                   "user_name TEXT, "
                   "crypto_address TEXT)")
    db.commit()


async def create_profile(user_id):
    user = cursor.execute("SELECT * FROM profile WHERE user_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cursor.execute("INSERT INTO profile (user_id) VALUES ({key})".format(key=user_id))
        db.commit()


async def edit_profile(state, user_id, user_name, crypto_address):
    cursor.execute("UPDATE profile SET user_name = '{}', crypto_address = '{}' WHERE user_id == '{}'".format(
        user_name, crypto_address, user_id))
    db.commit()


async def get_address(user_id):
    address = cursor.execute("SELECT crypto_address FROM profile WHERE user_id = ?", (user_id,)).fetchone()
    return address


async def get_user(user_id):
    user = cursor.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(key=user_id)).fetchone()
    return user


async def get_all_users(message: types.Message):
    cursor.execute("SELECT * FROM profile")
    results = cursor.fetchall()
    separator = '-' * 78
    if results:
        output_text = "Список полльзователей:\n"
        for row in results:
            output_text += (f"▫️ID: {row[0]}, Telegram ID: {row[1]}, Имя: {row[2]}\n"
                            f"Адрес кошелька: {row[3]}\n"
                            f"{separator}\n")

        await message.answer(output_text, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.answer("База данных пуста.")
