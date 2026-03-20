from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Личный кабинет')]
],
                        resize_keyboard=True,
                        input_field_placeholder='Выбирете пункт меню')


settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='💜WB', callback_data='wb'),
            InlineKeyboardButton(text='💙OZON', callback_data='ozon')
        ]
    ]
)

products = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🖥ТЕХНИКА', callback_data='tech')
        ],
        [
            InlineKeyboardButton(text='🎀ОДЕЖДА', callback_data='shirt')
        ],
        [
            InlineKeyboardButton(text='👞Обувь', callback_data='toof'),
        ],
        [
            InlineKeyboardButton(text='🍊Футболки', callback_data='tshirt')
        ],
        [
            InlineKeyboardButton(text='👖Штаны', callback_data='pants')
        ],
        [
            InlineKeyboardButton(text='🧢Аксесcуары', callback_data='akssesuars')
        ],
        [
            InlineKeyboardButton(text='🎁Подарки для мужчин🎩', callback_data='man_surprace')
        ],
        [
            InlineKeyboardButton(text='🎁Подарки для женщин👒', callback_data='woman_surpace')
        ],
        [
            InlineKeyboardButton(text='🎁Подарки для детей👶', callback_data='child_surpace')
        ],
        [
            InlineKeyboardButton(text='⚽Спорт', callback_data='sport')
        ],
        [
            InlineKeyboardButton(text='📕Книги', callback_data='books')
        ]
    ]
)