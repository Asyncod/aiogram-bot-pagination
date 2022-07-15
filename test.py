# -*- coding: utf-8 -*-
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from telegram_bot_pagination import InlineKeyboardPaginator
import config


#### PARAMETRS BOT'S ####
bot = Bot(config.bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

# Данные, которые вы будете отображать на страницах
# Количество страниц будет равно длине массива, подтягивать можно из БД
employer_data = ["Страница 1\n\nТекст текст текст текст текст текст текст",
                   "Страница 2\n\nТекст текст текст текст текст текст текст",
                   "Страница 3\n\nТекст текст текст текст текст текст текст",
                   "Страница 4\n\nТекст текст текст текст текст текст текст",
                   "Страница 5\n\nТекст текст текст текст текст текст текст",
                   "Страница 6\n\nТекст текст текст текст текст текст текст"]


@dp.message_handler(commands=["start"])
async def get_character(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton(text="Найти рект", callback_data="solana#1")
    keyboard.add(but1)

    await bot.send_message(chat_id=message.chat.id,
                           text=f"<b>Список деген минтов</b>\n\n"
                                f"Найди рект на солнае уже сегодня!\nТолько в нашей метавселенной!",
                           reply_markup=keyboard)


## Основная логика пагинации, сами поймете
@dp.callback_query_handler(lambda query: query.data.split("#")[0]=="solana")
async def characters_page_callback(query: types.CallbackQuery):
    page = int(query.data.split('#')[1])
    await send_character_page(query.message, page)


async def send_character_page(message, page):
    paginator = InlineKeyboardPaginator(
        page_count=len(employer_data),
        current_page=page,
        data_pattern="solana#{page}"
    )

    paginator.add_before(types.InlineKeyboardButton("Изучить проект", callback_data=f"work#{page}"))

    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=employer_data[page-1],
        reply_markup=paginator.markup,
        parse_mode="HTML"
    )


## Углубление в пагинацию, стоит добавить кнопку "Назад"
@dp.callback_query_handler(lambda query: query.data.split("#")[0]=="work")
async def inliner(query: types.CallbackQuery):
    employer_id = int(query.data.split('#')[1])
    await send_employer_id(query.message, employer_id)


async def send_employer_id(message, employer_id):
    await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.message_id,
        text=employer_data[employer_id-1], # Этот текст должен браться уже из другого массива, поставлено как пример
        parse_mode="HTML"
    )



#### BOT'S POLLING ####
if __name__ == '__main__':
    print("Bot work")
    executor.start_polling(dp)


# Считай что форк https://github.com/ksinn/python-telegram-bot-pagination