import requests
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import Command

from config import ETHERSCAN_API_KEY
from loader import dp


@dp.message(Command('gas'))
async def gas_command(message: types.Message):
    await on_gas_command(message)


async def on_gas_command(message: types.Message):
    url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey={ETHERSCAN_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data['status'] == '1':
        safe_low = data['result']['SafeGasPrice']
        fast = data['result']['FastGasPrice']
        await message.answer(text=f"💎Ethereum💎\n⛽️Gas: {safe_low} - {fast} Gwei⛽️", parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply("Не удалось получить данные.")
