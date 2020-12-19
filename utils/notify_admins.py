import logging

from aiogram import Dispatcher

from data.config import admins


async def on_shutdown_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот выключен!")

        except Exception as err:
            logging.exception(err)


async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin, "Бот запущен!")

        except Exception as err:
            logging.exception(err)


async def create_order_notify(dp: Dispatcher, customer_info):
    for admin in admins:
        try:
            order_message = [
                "ЗАКАЗ",
                f"Клиен: {customer_info['first_name']} {customer_info['last_name']}",
                f"Адрес: {customer_info['address']}",
                f"Количество пар обуви: {customer_info['count']}"
            ]
            await dp.bot.send_message(admin, '\n'.join(order_message))

        except Exception as err:
            logging.exception(err)
