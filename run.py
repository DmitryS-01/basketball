from aiogram import Bot, Dispatcher
from app.handlers import router

import asyncio

import logging

import os
import dotenv


async def main() -> None:
    dotenv.load_dotenv()
    bot = Bot(os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
