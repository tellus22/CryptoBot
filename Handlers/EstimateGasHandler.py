import web3
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from Blockchain.Extractor import get_fee_network, get_balance_usd
from Keyboards.Inline.CancelKeyboard import cancel_menu
from Keyboards.Inline.NetworksKeyboard import networks_menu, network_names
from Keyboards.Reply.MainKeyboard import main_keyboard
from States.GetFeeState import GetFeeState
from loader import dp


@dp.message(Command('estimate_gas'))
async def estimate_gas_command(message: types.Message, state: FSMContext):
    await message.answer("Выбери нужную сеть", reply_markup=networks_menu)
    await state.set_state(GetFeeState.get_kb)


@dp.callback_query(lambda query: query.data in network_names, GetFeeState.get_kb)
async def process_network_estimate_gas(callback_query: types.CallbackQuery, state: FSMContext):
    network_name = callback_query.data
    await state.update_data(network_name=network_name)
    await callback_query.message.answer(f"Введи количество для отправки в {network_name}", reply_markup=cancel_menu)
    # await callback_query.message.answer(f"Введи адресс с которого отправлять", reply_markup=cancelMenu)
    await state.set_state(GetFeeState.get_amount)
    # await getAmountState.getFromAddress.set()


# @dp.message_handler(state=getAmountState.getFromAddress)
# async def process_from_address(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     network_name = data.get('network_name')
#     from_address = message.text
#     await message.answer(f"Введи адресс куда отправлять", reply_markup=cancelMenu)
#     await state.update_data(network_name=network_name, from_address = from_address)
#     await getAmountState.getToAddress.set()
#
#
# @dp.message_handler(state=getAmountState.getToAddress)
# async def process_to_address(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     network_name = data.get('network_name')
#     from_address = data.get('from_address')
#     to_address = message.text
#     await message.answer(f"Введи количество для отправки в {network_name}", reply_markup=cancelMenu)
#     await state.update_data(network_name=network_name, from_address = from_address, to_address = to_address)
#     await getAmountState.getAmount.set()

@dp.message(GetFeeState.get_amount)
async def process_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    network_name = data.get('network_name')
    # from_address = data.get('from_address')
    # to_address = data.get('to_address')
    # await message.answer(f"from address - {from_address}, to address - {to_address}, network name - {network_name}")
    amount = message.text
    if amount.isdigit() or (amount.replace('.', '', 1).isdigit() and amount.count('.') == 1):
        try:
            fee = get_fee_network(network_name, amount)
            if fee is not None:
                await message.answer(f"💎{network_name}: {fee} 💎({get_balance_usd(network_name, fee)} USD)",
                                     reply_markup=main_keyboard())
            else:
                await message.answer("Указанная сеть не найдена.", reply_markup=main_keyboard())

        except web3.exceptions.ContractLogicError as e:
            await message.answer(f"Произошла ошибка: {e}", reply_markup=main_keyboard())

        except ValueError as e:
            await message.answer(f"Произошла ошибка: {e}", reply_markup=main_keyboard())
        await state.clear()
    else:
        await message.answer("Нормально введи!", reply_markup=cancel_menu)
        await state.set_state(GetFeeState.get_amount)
