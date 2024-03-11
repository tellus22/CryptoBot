from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Создание кнопки
cancel_button = InlineKeyboardButton(text="Отмена", callback_data="cancel_btn")

# Создание клавиатуры и добавление кнопки
cancel_menu = InlineKeyboardMarkup(inline_keyboard=[[cancel_button]])
