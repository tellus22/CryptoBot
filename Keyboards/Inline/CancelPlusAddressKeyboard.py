from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создание кнопок
my_address_button = InlineKeyboardButton(text="Мой адрес", callback_data="my_address_btn")
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel_btn")

# Создание клавиатуры и добавление кнопок
cancel_menu = InlineKeyboardMarkup(inline_keyboard=[[my_address_button], [cancel_button]])
