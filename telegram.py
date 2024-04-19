from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

import asyncio

from config import *
from database import *


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}!\nЯ буду вести всю твою баскетбольную стату!")




@dp.message()
async def message_handler(message: Message) -> None:
    user_id = message.from_user.id
    user_message = message.text
    user_dice = message.dice

    if user_dice:
        dice_type = user_dice.emoji
        score = user_dice.value
        if dice_type == '🏀':
            '''
            1 - отскочил от щита
            2 - покрутился и свалился
            3 - застрял 
            4 - покрутился и попал в корзину
            5 - попадание без касания кольца
            '''
            new_user(user_id)
            new_shot(user_id, 1)
            if score in [4, 5]:
                print('ХОРООООШ')
            else:
                print('не затащил((((')
        else:
            print('го лучше баскет(')

    if user_message:
        pass



async def main() -> None:
    bot = Bot(bot_token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
