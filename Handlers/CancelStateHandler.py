from aiogram import types
from aiogram.fsm.context import FSMContext

from loader import dp


@dp.callback_query(lambda query: query.data == 'cancel_btn')
async def cancel_inline_input(query: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await query.message.edit_text("Ввод отменен.\n/gas", reply_markup=None)
