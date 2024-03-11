from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from web3 import Web3

from Blockchain.Erc20Extractor import get_balance_erc20_tokens
from Blockchain.Erc721Excractor import get_balance_erc721_tokens
from Blockchain.Extractor import get_balance_network, get_balance_usd
from Database.MyDb import get_address
from Keyboards.Inline.CancelPlusAddressKeyboard import cancel_menu
from Keyboards.Inline.NetworksKeyboard import networks_menu, network_names
from Keyboards.Reply.MainKeyboard import main_keyboard
from States.GetBalanceState import GetBalanceState
from loader import dp


@dp.message(Command('balance'))
async def balance_command(message: types.Message, state: FSMContext):
    await message.answer("Выбери нужную сеть", reply_markup=networks_menu)
    await state.set_state(GetBalanceState.get_kb)


@dp.callback_query(lambda query: query.data in network_names, GetBalanceState.get_kb)
async def process_network_balance(callback_query: types.CallbackQuery, state: FSMContext):
    network_name = callback_query.data
    await state.update_data(network_name=network_name)
    await callback_query.message.answer(f"Введи адресс кошелька для проверки балланса в {network_name}",
                                        reply_markup=cancel_menu)
    await state.set_state(GetBalanceState.get_address)


@dp.message(GetBalanceState.get_address)
async def process_address(message: types.Message, state: FSMContext):
    data = await state.get_data()
    network_name = data.get('network_name')
    user_address = message.text

    if Web3.is_address(user_address):
        balance = get_balance_network(network_name, user_address)
        balance_usd = get_balance_usd(network_name, balance)
        token_balances = get_balance_erc20_tokens(network_name, user_address)
        nft_balances = get_balance_erc721_tokens(network_name, user_address)
        if balance is not None:
            response = f"💎{network_name}: {balance} ({balance_usd} USD)💎\n"

            for token_name, token_balance in token_balances.items():
                response += f"▫️{token_name} - {token_balance}\n"

            for nft_name, nft_balance in nft_balances.items():
                response += f"▫️(Nft) {nft_name} - {nft_balance}\n"

            await message.answer(response)

        else:
            await message.answer("Указанная сеть не найдена.", reply_markup=main_keyboard())
        await state.clear()
    else:
        await message.answer("Нормально введи!", reply_markup=cancel_menu)
        await state.set_state(GetBalanceState.get_address)


@dp.callback_query(lambda query: query.data == 'my_address_btn', GetBalanceState.get_address)
async def process_my_address(query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    network_name = data.get('network_name')
    address = await get_address(user_id=query.from_user.id)
    user_address = address[0]
    if user_address is None:
        await state.clear()
        await query.message.edit_reply_markup()
        await query.message.answer("Нету сохраненного адреса\n/add_address")
    else:
        if Web3.is_address(user_address):
            balance = get_balance_network(network_name, user_address)
            balance_usd = get_balance_usd(network_name, balance)
            token_balances = get_balance_erc20_tokens(network_name, user_address)
            nft_balances = get_balance_erc721_tokens(network_name, user_address)
            if balance is not None:
                response = f"💎{network_name}: {balance} ({balance_usd} USD)💎\n"

                for token_name, token_balance in token_balances.items():
                    response += f"▫️{token_name} - {token_balance}\n"

                for nft_name, nft_balance in nft_balances.items():
                    response += f"▫️(Nft) {nft_name} - {nft_balance}\n"

                await query.message.answer(response)

            else:
                await query.message.answer("Указанная сеть не найдена.")
            await state.clear()
        else:
            await query.message.answer("Нормально введи!")
            await state.set_state(GetBalanceState.get_address)
