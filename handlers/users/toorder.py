from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data import database
from loader import dp
from utils import notify_admins
from utils.misc import rate_limit
from states.order import Order

db = database.DBCommands()


@rate_limit(5, 'start')
@dp.message_handler(CommandStart(), state=None)
async def bot_start(message: types.Message):
    text = [
        'Здравствуйте!',
        'Введите, пожалуйста, адрес проживания'
    ]
    await message.answer('\n'.join(text))
    await Order.P1.set()


@dp.message_handler(state=Order.P1)
async def get_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await message.answer('Введите, пожалуйста, количесто пар обуви')
    await Order.next()


@dp.message_handler(state=Order.P2)
async def get_address(message: types.Message, state: FSMContext):
    count = message.text
    await state.update_data(count=count)

    data = await state.get_data()
    address = data.get('address')
    count = data.get('count')
    customer_info = {
        'count': count,
        'address': address,
        'last_name': message.chat.last_name,
        'first_name': message.chat.first_name
    }

    user = await db.add_new_user()
    order = await db.add_new_order(count=int(count), address=address)

    await notify_admins.create_order_notify(dp, customer_info)

    await message.answer(
        'Ваш заказ отправлен на обработку, вам перезвонит администратор, чтобы подтвердить заказ'
    )

    await state.finish()
