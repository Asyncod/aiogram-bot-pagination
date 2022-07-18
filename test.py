# -*- coding: utf-8 -*-
from aiogram.utils.exceptions import MessageNotModified
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
from telegram_bot_pagination import InlineKeyboardPaginator
import config


#### PARAMETRS BOT'S ####
bot = Bot(config.bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

## All data for page in pagin
employer_data = ["Страница 1\n\nТекст текст текст текст текст текст текст",
                   "Страница 2\n\nТекст текст текст текст текст текст текст",
                   "Страница 3\n\nТекст текст текст текст текст текст текст",
                   "Страница 4\n\nТекст текст текст текст текст текст текст",
                   "Страница 5\n\nТекст текст текст текст текст текст текст",
                   "Страница 6\n\nТекст текст текст текст текст текст текст"]


## Starting pagin
@dp.message_handler(commands=["start"])
async def get_character(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton(text="Найти рект", callback_data="solana#1")
    keyboard.add(but1)

    await bot.send_message(chat_id=message.chat.id,
                           text=f"<b>Список деген минтов</b>\n\n"
                                f"Найди рект на солнае уже сегодня!\nТолько в нашей метавселенной!",
                           reply_markup=keyboard)


## Main Logic one
@dp.callback_query_handler(lambda query: query.data.split("#")[0]=="solana")
async def characters_page_callback(query: types.CallbackQuery):
    page = int(query.data.split("#")[1])
    try:
        await send_character_page(query.message, page)
    except MessageNotModified:
        await bot.answer_callback_query(callback_query_id=query.id, text="Вы уже находитесь на этой странице",
                                        show_alert=True)


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


## Main Logic two
@dp.callback_query_handler(lambda query: query.data.split("#")[0]=="work")
async def inliner(query: types.CallbackQuery):
    employer_id = int(query.data.split("#")[1])

    keyboard = types.InlineKeyboardMarkup()
    but1 = types.InlineKeyboardButton(text="Назад", callback_data=f"solana#{employer_id}")
    keyboard.add(but1)

    await bot.edit_message_text(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id,
        text=employer_data[employer_id-1],
        parse_mode="HTML",
        reply_markup=keyboard
    )



#### BOT'S POLLING ####
if __name__ == '__main__':
    print("Bot work")
    executor.start_polling(dp)
