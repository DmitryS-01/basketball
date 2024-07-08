import asyncio
from datetime import datetime as dt

import aiogram.exceptions
from aiogram import Router
from aiogram.types import Message, MessageReactionUpdated, FSInputFile
from aiogram.filters import Command

from app.config import ADMIN_ID

from app.handlers.handlers import cmd_start

from app.database.database_funcs import get_all_users_ids, get_data, update_data

from app.states.admin_states import MessageToAnotherUser
from aiogram.fsm.context import FSMContext


router = Router()
router.message.filter(lambda message: message.from_user.id == ADMIN_ID)


@router.message(Command('start'))
async def admins_capabilities(message: Message) -> None:
    await cmd_start(message=message)
    await message.answer(text='<u><b>АДМИНСКИЕ КОМАНДЫ:</b></u> \n'
                              '\n'
                              '<u>/start</u> - показать дополнительные команды админа \n'
                              '<u>/all_data_export</u> - посмотреть информацию обо всех пользователях, '
                              'получить файл БД \n'
                              '/user_data {id пользователя} {характеристика / название столбца в БД} - '
                              'получить данные пользователя \n'
                              '/update_data {id пользователя} {характеристика / название столбца в БД} '
                              '{новое значение} - изменить данные пользователя \n'
                              '\n'
                              '<u>/send</u> - следующим сообщением отправьте то, что улетит всем (рассылка)',
                         parse_mode='HTML')


@router.message(Command('all_data_export'))
async def users_info_check(message: Message) -> None:
    date, hour, minute, second = dt.utcnow().date(), dt.utcnow().hour, dt.utcnow().minute, dt.utcnow().second
    await message.answer_document(FSInputFile(path="app/database/users.db",
                                              filename=f'{date}__{hour}_{minute}_{second}__bot_users_data'))


@router.message(Command('user_data'))
async def get_users_data(message: Message) -> None:
    try:
        data = message.text.split()
        tg_id, column_name = int(data[1]), data[2]
        users_data = get_data(tg_id=tg_id, column_name=column_name)
        await message.reply(text=f'{users_data}')
    except Exception as e:
        await message.reply(text=f'<u><b>ОШИБКА!!!</b></u> \n'
                                 f'{e}',
                            parse_mode='HTML')


@router.message(Command('update_data'))
async def update_users_data(message: Message) -> None:
    try:
        data = message.text.split()
        tg_id, column_name, new_value = int(data[1]), data[2], ' '.join(data[3:])
        if column_name in ["tg_id", "hits", "tries", "is_public", "is_not_banned"]:
            if type(new_value) not in [int]:
                raise TypeError("Неправильный тип данных!")
        elif column_name in ["hit_rate"]:
            if not new_value.replace('.', '', 1).isdigit():
                raise TypeError("Неправильный тип данных!")
        update_data(tg_id=tg_id, column_name=column_name, new_value=new_value)
        users_data = get_data(tg_id=tg_id, column_name=column_name)
        await message.reply(text=f'<u><b>Обновленные данные:</b></u> \n'
                                 f'{users_data}',
                            parse_mode='HTML')
    except Exception as e:
        await message.reply(text=f'<u><b>ОШИБКА!!!</b></u> \n'
                                 f'{e}',
                            parse_mode='HTML')


@router.message(Command('send'))
async def sending_message_to_user(message: Message, state: FSMContext) -> None:
    await state.set_state(MessageToAnotherUser.msg)
    await message.reply(text='Отправьте сообщение, которое хотите отправить! (<u>/cancel</u> - отмена)',
                        parse_mode='HTML')


@router.message(MessageToAnotherUser.msg, Command('cancel'))
async def sending_cancelling(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.reply(text='Отменено!')


@router.message(MessageToAnotherUser.msg)
async def text_of_message_to_another_user(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.reply(text='Через 15 секунд <u>ЭТО</u> сообщение будет отправлено! Удалите его для отмены!',
                        parse_mode='HTML')

    await asyncio.sleep(15)

    try:
        await message.reply(text='Начинаю отправку...')
        success_cnt = 0
        total_cnt = 0
        for user in get_all_users_ids():
            try:
                await message.send_copy(chat_id=user)
                success_cnt += 1
            except Exception as e:
                pass
            finally:
                total_cnt += 1
        await message.answer(text=f'Успешно отправлено {success_cnt} пользователям из {total_cnt}')
    except Exception as e:
        if str(e) == 'Telegram server says - Bad Request: message to be replied not found':
            await message.answer(text='Отменено!')
        else:
            await message.answer(text=f'{e}')


# TODO добавить баны(is_not_banned),
#  переделать архитектуру бота,
#  добавить в БД сведения о типе данных и в обновление данных встроить проверку на соответствие (F11)
