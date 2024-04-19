from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

import asyncio

from random import *

from config import bot_token
from database import *


async def main() -> None:
    bot = Bot(bot_token)
    await dp.start_polling(bot)


def random_num():
    win_nums = [1, 2, 3, 4]
    return randrange(1, 11) in win_nums


dp = Dispatcher()

its_a_hit = ['ХОРОООООШ!!!!', 'просто лучший!', 'ЛЕГЕНДА!!!!', 'сегодня ты просто демон 👿',
             'БУДЬ Я МАТЕРИАЛЬНЫМ, Я БЫ ТЕБЕ ДАЛ!', 'ВАУ!',
             '🏀', '🏀', '🏀', '🏀', '🏀']
oh_u_missed = ['главное не расстраиваться(', 'почти попал брат', 'ничего страшного, я тоже не всегда попадаю',
               '🏀', '🏀', '🏀']


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {message.from_user.full_name}!\n"
                         f"Я буду вести всю твою баскетбольную стату!\n"
                         f"Напиши '/my_stats' чтобы ее посмотреть 😘")


@dp.message()
async def message_handler(message: Message) -> None:
    user_id = message.from_user.id
    user_message = message.text
    user_dice = message.dice

    if message.text == '/my_stats':
        try:
            tries, points = data(user_id)
            hit_percentage = f'Процент попаданий - {round((points / tries) * 100, 2)}% !' if tries >= 15 else \
                f'Чтобы узнать более подробную статистику, соверши не менее 15 бросков!'
            await message.reply(f'Твоя статистика 🏀:\n'
                                f'Попаданий - {points}, всего бросков - {tries}\n'
                                f'{hit_percentage}')
        except Exception as e:
            print(f'{e}')

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
            new_shot(user_id, int(score in [4, 5]))

            await asyncio.sleep(5)
            if score in [4, 5]:
                try:
                    await message.reply(choice(its_a_hit))
                except Exception as e:
                    print(f'{e}')
            else:
                try:
                    if random_num():
                        await message.reply(choice(oh_u_missed))
                except Exception as e:
                    print(f'{e}')
        else:
            pass

    if user_message:
        pass


if __name__ == "__main__":
    asyncio.run(main())
