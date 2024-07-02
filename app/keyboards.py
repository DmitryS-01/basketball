import os
import dotenv

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


# кнопка броска мяча и ее эволюция

basketball_emoji_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='🏀')
    ]
],
    resize_keyboard=True,
    input_field_placeholder='Отправь "🏀" для броска!'
)

basketball_emoji_cooldown_keyboard = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Перезарядка...')
    ]
],
    resize_keyboard=True,
    input_field_placeholder='Подожди немного...'
)

# изменения профиля
profile_editing = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Изменить имя',
                             callback_data='changing_name'),
        InlineKeyboardButton(text='Изменить параметры видимости своего профиля',
                             callback_data='changing_profile_visibility')
    ],
    [
        InlineKeyboardButton(text='Подробнее про эти настройки и видимость профиля',
                             callback_data='profile_visibility_info')
    ]
]
)

profile_visibility_settings = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Общедоступный',
                             callback_data='public_profile_type_chosen'),
        InlineKeyboardButton(text='Приватный',
                             callback_data='private_profile_type_chosen')
    ],
    [
        InlineKeyboardButton(text='Подробнее про этот параметр',
                             callback_data='profile_visibility_info')
    ],
    [
        InlineKeyboardButton(text='Отменить изменения этого параметра',
                             callback_data='profile_visibility_editing_cancelled')
    ]
]
)

# кнопка связи с админом (используется в /help)
dotenv.load_dotenv()
admin_contact = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Админ всемогущий 🙏👊🤝',
                             url=f'https://t.me/{os.getenv('ADMIN_USERNAME')}')
    ]
]
)
