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

    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    # TODO пофиксить что при спаме мячиками тг ниче не обрабатывает и ломает стату
    asyncio.run(main())
