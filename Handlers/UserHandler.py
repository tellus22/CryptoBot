from aiogram import types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from web3 import Web3

from Database.MyDb import create_profile, edit_profile, get_address
from Keyboards.Inline.CancelKeyboard import cancel_menu
from Keyboards.Reply.MainKeyboard import main_keyboard
from States.AddUserState import AddUserState
from loader import dp


@dp.message(CommandStart())
async def process_start_command(message: types.Message):
    await message.answer("Привет!", parse_mode='HTML', reply_markup=main_keyboard())
    await create_profile(message.from_user.id)


@dp.message(Command('add_address'))
async def address_command(message: types.Message, state: FSMContext):
    await message.answer("Введи свой адресс по умолчанию", reply_markup=cancel_menu)
    await state.set_state(AddUserState.get_address)


@dp.message(AddUserState.get_address)
async def process_address(message: types.Message, state: FSMContext):
    answer = message.text
    if Web3.is_address(answer):
        userAddress = Web3.to_checksum_address(answer)
        await edit_profile(state, user_id=message.from_user.id, user_name=message.from_user.full_name,
                           crypto_address=userAddress)
        await message.answer("Успешно добавлен!")
        await state.clear()
    else:
        await message.answer("Нормально введи")


@dp.message(Command('get_address'))
async def get_address_command(message: types.Message):
    address = await get_address(user_id=message.from_user.id)
    user_address = address[0]
    if user_address is None:
        await message.answer("Нету сохраненного адреса\n/add_address")
    else:
        await message.answer(f"<pre>{user_address}</pre>\n"
                             f"Eсли хочешь обновить адрес - введи команду /add_address", parse_mode='HTML')
