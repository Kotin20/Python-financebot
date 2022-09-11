from aiogram import executor
from create_bot import dp
from date_base import sqlite_db


async def on_startup(_):
	print("Бот запущен")
	sqlite_db.sql_start()

from handlers import client

client.register_handlers_client(dp)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup = on_startup)
