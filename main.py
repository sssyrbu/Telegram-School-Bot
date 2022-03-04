#!venv/bin/python

from config import tkn
import logging
from aiogram import Bot, Dispatcher, executor, types
import aiogram.utils.markdown as fmt
from sys import exit
import emoji

# Импорт диалоговой базы знаний
from queries import holiday_queries, doctor_cabinet_queries, contacts_queries, exams_queries, dining_room_queries, \
    documents_queries, future_student_school_queries, news_queries

TOKEN = tkn
if not TOKEN:
    exit("Error: no token provided")
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)

dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


# Приветствие пользователя
@dp.message_handler(commands=["start"])
async def greeting(message: types.Message):
    user_name = message.from_user
    await message.answer(f"Здравствуйте, {user_name['first_name']}!"
                         f" Я бот-помощник МБОУ СШ №45, вы можете задать мне интересующие вас вопросы. Вы можете "
                         f"обращаться ко мне по следующим вопросам: график работы школы, медицинский кабинет, "
                         f"питание в столовой, документы для обучения в нашей школе, "
                         f"даты проведения государственных экзаменов, "
                         f"'Школа будущего первоклассника', новости школы и контакты для связи.")


# Обработка запросов
@dp.message_handler()
async def queries_handler(message: types.Message):
    # Обработка запросов, связанных с каникулами и графиком работы школы
    msg = message.text.lower()
    for query in holiday_queries:
        if query in msg:
            await message.answer(
                fmt.text(
                    fmt.text(fmt.hbold(emoji.emojize(":calendar: Календарный график работы школы:"))),
                    fmt.text(fmt.hitalic(emoji.emojize(":white_small_square: I четверть")),
                             " 01 сентября - 30 октября. Каникулы: с 01 ноября по 07 ноября."),
                    fmt.text(fmt.hitalic(emoji.emojize(":white_small_square: II четверть")),
                             "08 ноября - 28 декабря. Каникулы: с 29 декабря по 09 января"),
                    fmt.text(fmt.hitalic(emoji.emojize(":white_small_square: III четверть")),
                             "10 января - 19 марта. Каникулы: с 21 марта по 27 марта. " 
                             "(доп. каникулы для 1-х классов: 21.02 - 27.02.2022)"),
                    fmt.text(fmt.hitalic(emoji.emojize(":white_small_square: IV четверть")),
                             "28 марта - 29 мая (1-8, 10 кл.), "
                             "28 марта - 25 мая (9, 11 кл.)"),
                    fmt.text(fmt.hitalic("Выходные и праздничные дни: 23.02, 08.03, 02-03.05, 09-10.05.2022")),
                    sep="\n"
                ), parse_mode="HTML"
            )
    # Обработка запросов, связанных с мед.кабинетом
    for query in doctor_cabinet_queries:
        if query in msg:
            await message.answer(
                fmt.text(
                    fmt.text(fmt.hbold(emoji.emojize(":hospital: Часы работы медицинского кабинета"))),
                    fmt.text(emoji.emojize(":white_small_square: Понедельник: 8.30 - 16.00")),
                    fmt.text("(2-й, 4-й понедельник с 8.30 до 13.00)"),
                    fmt.text(emoji.emojize(":white_small_square: Вторник: 8.30 - 16.00")),
                    fmt.text(emoji.emojize(":white_small_square: Среда: 8.30 - 16.00")),
                    fmt.text("(1-я среда каждого месяца с 10.00 до 16.00)"),
                    fmt.text(emoji.emojize(":white_small_square: Четверг: 8.30 - 16.00")),
                    fmt.text(emoji.emojize(":white_small_square: Пятница: 8.30 - 16.00")),
                    fmt.text("Технологический перерыв, проветривание: 10.30 - 10.45, 12.30 - 13.00"),
                    fmt.text(fmt.hbold("Фельдшер - Ряхина Наталья Дмитриевна")),
                    sep="\n"
                ), parse_mode="HTML"
            )
    # Обработка запросов, связанных с контактной информацией
    for query in contacts_queries:
        if query in msg:
            await message.answer(
                fmt.text(
                    fmt.text(fmt.hbold(emoji.emojize(":telephone_receiver: Телефоны для связи"))),
                    fmt.text("Директор: Елькина Лидия Васильевна "), fmt.hitalic("23-67-31"),
                    fmt.text("Секретарь, вахта: ", fmt.hitalic("29-19-94")),
                    fmt.text("Заместитель директора и социальный педагог: ", fmt.hitalic("8 (818) 229 09-74")),
                    fmt.text("Заместитель директора по начальной школе:  ", fmt.hitalic("8 (818) 223 72-57")),
                    fmt.text("Библиотека: ", fmt.hitalic("8 (818) 223 72-57")),
                    sep="\n"
                ), parse_mode="HTML"
            )
    # Обработка запросов, связанных с экзаменами
    caption = emoji.emojize(":books: График проведения экзаменов на 2022 год")
    exams_photo = "https://static.ngs.ru/news/2015/99/preview/667d0a513a4c3b5b116fd230537660ec0c8c7a46_3000_2100.jpg"
    for query in exams_queries:
        if query in msg:
            await bot.send_photo(message.from_user.id, exams_photo, caption=caption)

    # Обработка запросов, свзязанных с приёмом документов в 1 класс
    for query in documents_queries:
        if query in msg:
            await message.answer(
                fmt.text(
                    fmt.text(emoji.emojize(":open_file_folder: Приём документов в первый класс проходит"
                                           " с 1 апреля по 30 июня 2022 года.")),
                    fmt.text("Для более подробной информации свяжитесь с нашей школой (список контактов для связи можно"
                             "попросить у бота напрямую)"),
                    sep="\n"
                ), parse_mode="HTML"
            )

    # Обработка запросов, связанных с школьной столовой
    for query in dining_room_queries:
        if query in msg:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            buttons = ["1-4", "5-11"]
            keyboard.add(*buttons)
            await message.answer("Питание может различатся в зависимости от класса. В каком классе вы/ваш ребенок?",
                                 reply_markup=keyboard)

    primary_meals_link = "https://school45.1mcg.ru/data/5e5af101422528d95b452e66fed4d5bd.pdf"
    high_meals_link = "https://school45.1mcg.ru/data/0c7990b66f8c954fba39e2b7a07e7643.pdf"
    if msg == "1-4":
        await message.answer(f"С планом питания учеников 1-4 классов вы можете ознакомиться, перейдя по ссылке: "
                             f"{primary_meals_link}")
    elif msg == "5-11":
        await message.answer(f"С планом питания учеников 5-11 классов вы можете ознакомиться, перейдя по ссылке: "
                             f"{high_meals_link}")

    for query in future_student_school_queries:
        if query in msg:
            await message.answer(
                fmt.text(
                    fmt.text("Школа будущего первоклассника - это проект МБОУ СШ №45, в рамках которого будущие "
                             "первоклассники могут подготовиться к обучению в школе."),
                    fmt.text("С памяткой для родителей и графиком проведения занятий можно ознакомиться"),
                    fmt.text(fmt.hlink("по ссылке",
                                       "https://docs.google.com/document/d/1djjXLOAj49lstk9dfLS3ITzOYLegvesL/edit")),
                    sep="\n"
                ), parse_mode="HTML"
            )

    for query in news_queries:
        if query in msg:
            await message.answer(
                fmt.text(
                    fmt.text(emoji.emojize(":newspaper: Новости школы можно узнать")),
                    fmt.text(fmt.hlink("по ссылке", "https://school45.1mcg.ru/Novosti"))
                ), parse_mode="HTML"
            )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
