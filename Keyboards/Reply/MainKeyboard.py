from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def main_keyboard():
    main_kb = ReplyKeyboardBuilder()

    main_kb.button(text='/gas')
    main_kb.button(text='/balance')
    main_kb.button(text='/swap_0')
    main_kb.button(text='/estimate_gas')
    main_kb.button(text='/get_address')
    main_kb.button(text='/add_address')
    main_kb.adjust(2)
    return main_kb.as_markup()

# # Создание кнопок
# gas_eth_btn = KeyboardButton(text='/gas')
# balance_btn = KeyboardButton(text='/balance')
# swap_btn = KeyboardButton(text='/swap_0')
# estimate_gas_btn = KeyboardButton(text='/estimate_gas')
# get_address_btn = KeyboardButton(text='/get_address')
# add_address_btn = KeyboardButton(text='/add_address')
#
# # Создание клавиатуры
# main_kb_markup = ReplyKeyboardMarkup(resize_keyboard=True)
# main_kb_markup.row(gas_eth_btn, balance_btn)
# main_kb_markup.row(swap_btn, estimate_gas_btn)
# main_kb_markup.row(get_address_btn, add_address_btn)
