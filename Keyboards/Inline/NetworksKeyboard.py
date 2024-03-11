# from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# from Blockchain.Extractor import get_networks_name
#
# network_names = get_networks_name()
#
# networks_menu = InlineKeyboardMarkup(inline_keyboard=[])
#
# for network_name in network_names:
#     button = InlineKeyboardButton(text=network_name, callback_data=network_name)
#     networks_menu.inline_keyboard.append([button])
#
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Blockchain.Extractor import get_networks_name

network_names = get_networks_name()

networks_menu = InlineKeyboardMarkup(inline_keyboard=[])

# Разбиваем список кнопок на подсписки по две кнопки
buttons = [InlineKeyboardButton(text=network_name, callback_data=network_name) for network_name in network_names]
buttons_per_row = 2
button_groups = [buttons[i:i+buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]

# Добавляем подсписки кнопок в inline_keyboard
for group in button_groups:
    networks_menu.inline_keyboard.append(group)
