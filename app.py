async def on_startup(dp):
    import filters
    import middlewares
    from data.database import create_db
    await create_db()
    filters.setup(dp)
    middlewares.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)


async def on_shutdown(dp):
    from utils.notify_admins import on_shutdown_notify

    await on_shutdown_notify(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
