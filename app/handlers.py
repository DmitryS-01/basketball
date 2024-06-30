from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, ReactionTypeEmoji
from aiogram import F

from aiogram.fsm.context import FSMContext

from aiogram import Router

import asyncio

import random

from app.database.database_funcs import new_user, update_data, get_data, global_top
from app.keyboards import basketball, profile_editing, profile_visibility_settings, admin_contact
from app.FSM import ProfileEditing


router = Router()


scored_text = ['ХОРОООООШ!!!!', 'ЛУЧШИЙ!', 'ЛЕГЕНДА!!!!', 'СЕГОДНЯ ТЫ ПРОСТО ДЕМОООН! 👹', 'G.O.A.T. !', 'ВАУ!', '🏀']
scored_emoji = ['😎', '😍', '🤩', '🔥', '❤️‍🔥']
didnt_scored_emoji = ['😭', '💔', '😢']


# перезапуск бота и выдача клавы с 🏀
@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.reply_photo(photo='https://www.google.com/imgres?q=%D0%B1%D0%B0%D1%81%D0%BA%D0%B5%D1%82%D0%B1%D0%BE'
                                    '%D0%BB%20%D1%81%D1%83%D0%B4%D1%8C%D1%8F&imgurl=https%3A%2F%2Fwww.ballgames.ru'
                                    '%2Fimg%2Fbasketball_referi_h4-1.jpg&imgrefurl=https%3A%2F%2Fwww.ballgames.ru%2F'
                                    '%25D0%25B1%25D0%25B0%25D1%2581%25D0%25BA%25D0%25B5%25D1%2582%25D0%25B1%25D0%25BE'
                                    '%25D0%25BB%2F%25D0%25BF%25D1%2580%25D0%25B0%25D0%25B2%25D0%25B8%25D0%25BB%25D0'
                                    '%25B0_%25D0%25B1%25D0%25B0%25D1%2581%25D0%25BA%25D0%25B5%25D1%2582%25D0%25B1'
                                    '%25D0%25BE%25D0%25BB%25D0%25B0%2F%25D1%2581%25D1%2583%25D0%25B4%25D0%25B5%25D0'
                                    '%25B9%25D1%2581%25D1%2582%25D0%25B2%25D0%25BE_%25D0%25B2_%25D0%25B1%25D0%25B0'
                                    '%25D1%2581%25D0%25BA%25D0%25B5%25D1%2582%25D0%25B1%25D0%25BE%25D0%25BB%25D0%25B5'
                                    '%2F&docid=y2_O36kwJcuISM&tbnid=63Ke7nnQCIoFxM&vet=12ahUKEwjt'
                                    '-o_yoISHAxVaKRAIHZTlBrUQM3oECBoQAA..i&w=1024&h=683&hcb=2&ved=2ahUKEwjt'
                                    '-o_yoISHAxVaKRAIHZTlBrUQM3oECBoQAA',
                              caption=f'Привет, <b>{message.from_user.full_name}</b>! Это бот-баскетболист! 😎 \n'
                                      f'\n'
                                      f'Я буду вести статистику твоих бросков! Отправляй в чат со мной "🏀", а я буду '
                                      f'фиксировать твои результаты! \n'
                                      f'[бот <i><b>ПОКА ЧТО</b></i> не может анализировать твою игру в реальной жизни, '
                                      f'но покажет твои умения в баскетболе версии Telegram 😀]',
                              parse_mode='HTML',
                              reply_markup=basketball)
    await message.answer(text='Доступные тебе команды ты можешь посмотреть в Меню слева от клавиатуры! '
                              'Продублирую их для твоего удобства 😘 : \n'
                              '\n'
                              '/start покажет тебе эти сообщения и может помочь решить некоторые баги \n'
                              '/my_stats позволит посмотреть статистику твоих бросков и аналитику по ним \n'
                              '/my_account поможет настроить видимость твоих достижений другими пользователями \n'
                              '/global_top покажет топ игроков с самым большим процентом попаданий \n'
                              '/help поможет решить любые проблемы <i>(ты сможешь связаться с админом!)</i> \n'
                              '/future_drops расскажет о будущих обновлениях бота \n'
                              'Кроме того, у тебя в клавиатуре выведена кнопка "🏀", с помощью которой '
                              'ты сможешь быстро совершить бросок в кольцо! \n'
                              '\n'
                              'Это все доступные на данный момент функции, но умения бота непрерывно совершенствуются! '
                              'Приятного пользования, БРО! 👊',
                         parse_mode='HTML')
    tg_username = message.from_user.username if message.from_user.username is not None else ''
    new_user(tg_id=message.from_user.id, tg_username=tg_username, users_name=message.from_user.full_name)


# показ статистики попаданий пользователя
@router.message(Command('my_stats'))
async def cmd_users_stats(message: Message) -> None:
    hits = get_data(tg_id=message.from_user.id, value_name='hits')
    tries = get_data(tg_id=message.from_user.id, value_name='tries')
    hit_rate = f'<b>Процент попаданий</b> - {get_data(tg_id=message.from_user.id, value_name='hit_rate')}% !' \
        if tries >= 15 else \
        (f'Чтобы узнать более подробную статистику, соверши не менее 15 бросков! Жми на кнопку "🏀" клавиатуры, чтобы '
         f'совершить бросок!')
    await message.reply(text=f'<u><b>Твоя статистика 🏀:</b></u>\n'
                             f'\n'
                             f'<b>Попаданий</b> - {hits} \n'
                             f'<b>Всего бросков</b> - {tries} \n'
                             f'\n'
                             f'{hit_rate}',
                        parse_mode='HTML')


# изменение параметров профиля (для видимости в глобальном топе)
@router.message(Command('my_account'))
async def cmd_users_profile(message: Message) -> None:
    name = get_data(tg_id=message.from_user.id, value_name='name')
    is_public = '✅Да' if get_data(tg_id=message.from_user.id, value_name='is_public') else '❌Нет'
    await message.reply(text=f'<u><b>Информация о тебе:</b></u>\n'
                             f'\n'
                             f'<b>Имя</b> - {name}\n'
                             f'<b>Распространение данных</b> - {is_public}',
                        parse_mode='HTML',
                        reply_markup=profile_editing)


# пользователь отменил внесение изменений в свой профиль
@router.callback_query(F.data == 'profile_visibility_editing_cancelled')
async def profile_editing_cancel(callback: CallbackQuery) -> None:
    await callback.answer(text='Изменения отменены!')
    await callback.message.answer(text='Вы отменили изменения профиля!\n'
                                       'Пропишите /my_account для возврата к редактированию профиля!')
    await callback.message.delete()


@router.message(Command('cancel'))
async def name_editing_cancelled(message: Message, state: FSMContext) -> None:
    if await state.get_state() == ProfileEditing.name:
        await message.answer(text='Вы отменили изменение имени профиля!\n'
                                  'Пропишите /my_account для возврата к редактированию профиля!')
        await state.clear()
    else:
        await message.reply(text='Сейчас эта команда недоступна!')


# изменение имени пользователя в боте
@router.callback_query(F.data == 'changing_name')
async def changing_name_button_pressed(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(text='')
    await callback.message.reply(text='Введи новое имя (/cancel для отмены):')
    await state.set_state(ProfileEditing.name)


@router.message(ProfileEditing.name)
async def new_name(message: Message, state: FSMContext) -> None:
    update_data(tg_id=message.from_user.id, value_name='name', new_value=message.text)
    await state.clear()
    await message.reply(text='Данные обновлены!')
    await cmd_users_profile(message=message)


# изменение параметров видимости профиля пользователя бота
@router.callback_query(F.data == 'changing_profile_visibility')
async def changing_profile_visibility_button_pressed(callback: CallbackQuery) -> None:
    await callback.answer(text='')
    await callback.message.answer(text='⚠️ Изменение параметров видимости профиля другими пользователями бота\n'
                                       '\n'
                                       'Выберите новый тип вашего профиля: 🔓 публичный (виден в общем топе) '
                                       'или 🔒 приватный (скрыт в топе пользователей):',
                                  reply_markup=profile_visibility_settings)
    await callback.message.delete()


@router.callback_query(F.data == 'public_profile_type_chosen')
async def public_profile_type_chosen(callback: CallbackQuery) -> None:
    await callback.answer(text='Принято!')
    await callback.message.answer(text='Ваш профиль общедоступен 🔓 и виден в топе пользователей!\n'
                                       'Для изменения других параметров введите /my_account !')
    await callback.message.delete()
    update_data(tg_id=callback.from_user.id, value_name='is_public', new_value=1)


@router.callback_query(F.data == 'private_profile_type_chosen')
async def private_profile_type_chosen(callback: CallbackQuery) -> None:
    await callback.answer(text='Принято!')
    await callback.message.answer(text='Ваш профиль скрыт 🔒 и <u><b>не</b></u> виден в топе пользователей!\n'
                                       'Для изменения других параметров введите /my_account !',
                                  parse_mode='HTML')
    await callback.message.delete()
    update_data(tg_id=callback.from_user.id, value_name='is_public', new_value=0)


# объяснение механики видимости профиля
@router.callback_query(F.data == 'profile_visibility_info')
async def profile_visibility_info(callback: CallbackQuery) -> None:
    await callback.answer(text='')
    await callback.message.reply(text='<u><b>❔ Дополнительная информация про топ пользователей бота:</b></u>\n'
                                      '\n'
                                      'Бот составляет статистику попаданий для каждого пользователя '
                                      'исходя из процента его попаданий.\n'
                                      'Далее бот формирует топ самых метких пользователей, '
                                      'доступный по команде /global_top.\n'
                                      'В этом топе видны только те пользователи, в профиле которых включен '
                                      'его показ; те, кто запретил демонстрацию статистике, '
                                      'в топе отображаться не будут.\n'
                                      '\n'
                                      '🏀 Поэтому если Вы хотите попасть в глобальный топ, то необходимо чтобы '
                                      'по команде /my_account отображалось следующее:\n'
                                      '<i><b>Распространение данных</b> - ✅Да</i>',
                                 parse_mode='HTML')


# вывод топа пользователей
@router.message(Command('global_top'))
async def cmd_show_top_players(message: Message) -> None:
    top_5_users = global_top()[:5]
    top_users_text = ['🏅 <u><b>Топ 5 пользователей с лучшими показателями попаданий:</b></u>', '\n']
    for position, user in enumerate(top_5_users):
        tg_id, tg_username, hit_rate, name = user
        link = f'@{tg_username}' if str(tg_username) != 'None' else '[у пользователя нет тэга Telegram]'
        top_users_text.append(f'<u>{position + 1}</u>. {name} {link} - <b>{hit_rate}%</b>')
    top_users_text.extend(['\n', 'Поздравляем победителей! 🎉'])
    await message.reply_photo(photo='https://www.google.com/imgres?q=nba%20%D0%BD%D0%B0%D0%B3%D1%80%D0%B0%D0%B6%D0%B4'
                                    '%D0%B5%D0%BD%D0%B8%D0%B5&imgurl=https%3A%2F%2Fphotobooth.cdn.sports.ru%2Fpreset'
                                    '%2Fpost%2Fa%2Fed%2Fe8644f09e421fa756a7dceb02f047.jpeg&imgrefurl=https%3A%2F'
                                    '%2Fwww.sports.ru%2Ftribuna%2Fblogs%2Fbasketblogg%2F2744167.html&docid=UXQ3C'
                                    '-KVGICdaM&tbnid=_-vdadFGB7_1eM&vet=12ahUKEwi-3dL0oYSHAxXOGRAIHSGYCxAQM3oECGwQAA'
                                    '..i&w=730&h=489&hcb=2&ved=2ahUKEwi-3dL0oYSHAxXOGRAIHSGYCxAQM3oECGwQAA',
                              caption='\n'.join(top_users_text),
                              parse_mode='HTML')


# вызов помощи
@router.message(Command('help'))
async def cmd_help(message: Message) -> None:
    await message.reply_photo(photo='https://www.google.com/imgres?q=%D1%81%D0%B0%D0%BD%D1%82%D0%B5%D1%85%D0%BD%D0%B8'
                                    '%D0%BA%20%D1%84%D0%BE%D1%82%D0%BE&imgurl=http%3A%2F%2Felovoinfo.ru%2Fwp-content'
                                    '%2Fuploads%2F2023%2F04%2F%25D0%2592%25D0%25B0%25D0%25BB%25D0%25B5%25D1%2580%25D0'
                                    '%25B8%25D0%25B9-%25D0%2594%25D1%2583%25D1%2580%25D0%25BD%25D0%25BE%25D0%25B2'
                                    '%25D1%2586%25D0%25B5%25D0%25B2-scaled.jpg&imgrefurl=https%3A%2F%2Felovoinfo.ru'
                                    '%2F%25D0%25BC%25D0%25BE%25D1%258F-%25D0%25BF%25D1%2580%25D0%25BE%25D1%2584%25D0'
                                    '%25B5%25D1%2581%25D1%2581%25D0%25B8%25D1%258F-%25D1%2581%25D0%25B0%25D0%25BD'
                                    '%25D1%2582%25D0%25B5%25D1%2585%25D0%25BD%25D0%25B8%25D0%25BA%2F&docid'
                                    '=jgeNM2fJhtbjKM&tbnid=nxoEyetud_0GQM&vet'
                                    '=12ahUKEwiyotWcooSHAxWSExAIHUseCroQM3oECBMQAA..i&w=2560&h=1707&hcb=2&ved'
                                    '=2ahUKEwiyotWcooSHAxWSExAIHUseCroQM3oECBMQAA',
                              caption=f'Если у тебя случился баг, попробуй перезапустить бота с помощью /start !\n'
                                      f'\n'
                                      f'Не помогло? Напиши админу <i>[на фото]</i>, он тебе поможет!\n'
                                      f'Твой id - <i><b>{message.from_user.id}</b></i>',
                              parse_mode='HTML',
                              reply_markup=admin_contact)


# новости и обновления бота
@router.message(Command('future_drops'))
async def future_drops(message: Message) -> None:
    await message.reply(text='Вижу ты неравнодушен ко мне! 😀😍🙏 Спасибо за любопытство! \n'
                             '\n'
                             'В будущих обновлениях я смогу анализировать броски более тщательно '
                             'по большему количеству параметров; обучусь новым командам иии...... '
                             '<span class="tg-spoiler">[что-то ОЧЕНЬ секретное!]</span> \n'
                             'Также в глобальных планах сделать криптовалюту на базе Ton и расширить '
                             'сферу деятельности бота за Telegram (возможно даже в реальную жизнь!) \n'
                             '\n'
                             'Из более реального и близкого - <b>добавление в бота новостей баскетбола,'
                             'введение системы сезонов с наградами!</b>\n'
                             '\n'
                             'Дальше много нового, не пропусти это! 🏀',
                        parse_mode='HTML')


# бросок 🏀
@router.message(F.dice)
async def basketball_msg(message: Message):
    if message.dice.emoji == '🏀':
        '''
        1 - отскочил от щита
        2 - покрутился и свалился
        3 - застрял
        4 - покрутился и попал в корзину
        5 - попадание без касания кольца
        '''
        current_hits = get_data(tg_id=message.from_user.id, value_name='hits')
        current_tries = get_data(tg_id=message.from_user.id, value_name='tries')
        await asyncio.sleep(5)

        update_data(tg_id=message.from_user.id, value_name='tries', new_value=current_tries + 1)
        if message.dice.value in [4, 5]:
            update_data(tg_id=message.from_user.id, value_name='hits', new_value=current_hits + 1)
            update_data(tg_id=message.from_user.id, value_name='hit_rate',
                        new_value=round((current_hits + 1) / (current_tries + 1) * 100, 2))
            await message.react([ReactionTypeEmoji(emoji=random.choice(scored_emoji))])
            if message.dice.value == 5:
                await message.reply(text=random.choice(scored_text))
        else:
            update_data(tg_id=message.from_user.id, value_name='hit_rate',
                        new_value=round(current_hits / (current_tries + 1) * 100, 2))
            await message.react([ReactionTypeEmoji(emoji=random.choice(didnt_scored_emoji))])
        await cmd_users_stats(message=message)
    else:
        await message.reply(text='Это ты не ко мне, я по баскетболу 😎\n'
                                 'Отправь "🏀", чтобы совершить бросок!')


# другие сообщения
@router.message()
async def unexpected_msg(message: Message) -> None:
    await message.react(reaction=[ReactionTypeEmoji(emoji='🤔')])
