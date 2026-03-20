from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

import app.keyboards as kb
from config import ADMIN_ID

from parsers import parse_wb_product, parse_ozon_product, CATEGORIES

router = Router()

users = set()
start_count = 0
help_count = 0

@router.message(CommandStart())
async def cmd_start(message: Message):
    global start_count

    user_id = message.from_user.id

    start_count += 1

    users.add(user_id)

    await message.answer(
        f'😊Привет {message.from_user.first_name}!\n'
        'Я бот 💻парсер. Помогу теме найти товары не заходя на маркетплейс.\n'
        '📞Если нужна будет помощь в использовании пишите /help\n\n'
        'Выберете опцию:\n',
        reply_markup = kb.settings
    )


# handlers.py

...

@router.callback_query(lambda c: c.data in ['wb', 'ozon'])
async def handle_marketplace_callback(callback_query: types.CallbackQuery):
    await callback_query.answer('Обработка...')

    marketplace = callback_query.data

    await callback_query.message.answer(
        '✔ ОПЦИЯ ВЫБРАНА\n\n'
        'Выберите тип продукта, который хотите найти:',
        reply_markup=kb.products
    )

@router.callback_query(lambda c: c.data in CATEGORIES.keys())
async def handle_product_type_callback(callback_query: types.CallbackQuery):
    category = callback_query.data  # Выбранная категория (например, tech, shirt...)
    marketplace = None  # Здесь будем хранить ранее выбранную площадку (wb или ozon)

    # Определяем выбранную площадку (marketplace) из предыдущего шага
    previous_message_text = callback_query.message.text
    if 'ОПЦИЯ ВЫБРАНА' in previous_message_text:
        marketplace = previous_message_text.split('\n')[0].split()[-1]

    if not marketplace or marketplace not in ('wb', 'ozon'):
        await callback_query.answer('Ошибка: неизвестная площадка.')
        return

    # Используем соответствующий парсер для выбранного маркета
    parser_func = (
        parse_wb_product if marketplace == 'wb' else
        parse_ozon_product
    )

    url = CATEGORIES[category][marketplace]
    results = parser_func(url)

    answer_text = ''
    for idx, product in enumerate(results[:5], start=1):
        answer_text += f"{idx}. Название: {product['title']}\nЦена: {product['price']} ₽\nАртикул: {product['article']}\nСклад: {product['stock'] or 'Нет информации'}\n\n"

    await callback_query.message.answer(answer_text)

@router.message(Command('help'))
async def cmd_help(message: Message):
    global help_count

    user_id = message.from_user.id

    help_count += 1

    users.add(user_id)

    await message.reply(
        '❗КАК ПОЛЬЗОВАТЬСЯ ДАННЫМ ЧАТ-БОТОМ❗\n\n'
        'Здравствуйте уважаемый пользователь! Данный бот был создан для быстрого поиска товаров на платформах Wildberries и Ozon.\n'
        'Бот безопасно парсирует данные с сайтов не нарушая правил.\n\n'
        '   1.Чтобы пользоваться ботом вам нужно выбрать маркетплейс, на котором хотите посмотреть товары(WB/OZON).\n'
        '   2.Выберите категорию товаров, которую хотите просмотреть(Техника/Одежда/Обувь и тому подобное...).\n'
        '   3.Бот выдаёт список проверенных продавцов с хорошим товаром\n\n'
        'НАЖМИТЕ НА /start, ЧТОБЫ ВЕРНУТЬСЯ ОБРАТНО.'
    )
@router.message(Command('admin'))
async def admin_panel(message: Message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID:
        await message.reply('❌Вы не можете использовать данную команду.')
    else:
        await message.reply(
            '✔УСПЕШНО\n\n'
            'Здравствуйте Иван! Добро пожаловать в админ-панель.\n\n'
            '📊 СТАТИСТИКА:\n'
            f'💎Уникальные пользователи: {len(users)}\n'
            f'🚀Всего запусков: {start_count}\n'
            f'🆘Количество /help: {help_count}\n'
        )