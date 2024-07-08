from aiogram import Bot, Dispatcher
from app.handlers.admin_commands_handlers import router as admin_router
from app.handlers.handlers import router

import asyncio

import logging

from app.config import BOT_TOKEN


async def main() -> None:
    bot = Bot(BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(router)

    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
