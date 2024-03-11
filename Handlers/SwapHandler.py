from aiogram import types
from aiogram.filters import Command

from Blockchain.Uniswap import allowance, swap, approve, transaction_status
from config import ADMIN_CHAT_ID
from loader import dp

token_out = '0xB4FBF271143F4FBf7B91A5ded31805e42b2208d6'
token_in = '0x252d98fab648203aa33310721bbbddfa8f1b6587'
value = 0.01


@dp.message(Command('swap'))
async def swap_command(message: types.Message):
    if message.from_user.id == ADMIN_CHAT_ID:
        if allowance(token_out) <= value * 1.1:
            await message.answer("Need approval")
            await message.answer(f"Hash - {approve(token_out)}")
            await message.answer(f"Allowance = {allowance(token_out)}")
            await message.answer(f"Hash - {swap(token_out, token_in, value)}")
        else:
            await message.answer(f"Allowance = {allowance(token_out)}")
            await message.answer(f"Hash - {swap(token_out, token_in, value)}")
    else:
        await message.answer("ты не админ", parse_mode='HTML')

    # tx_status = transaction_status(f'{approve(token_out)}')
    # if tx_status == 1:
    #     await message.answer("Transaction status - <b>True</b>", parse_mode='HTML')
    # else:
    #     await message.answer("Transaction status - <b>False</b>", parse_mode='HTML')
