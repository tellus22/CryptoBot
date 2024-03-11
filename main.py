import asyncio

from Database.MyDb import db_start
from Handlers import dp
from Handlers.AdminHandler import admin_message
from loader import bot


async def main() -> None:
    await admin_message()
    await db_start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.run(main())
