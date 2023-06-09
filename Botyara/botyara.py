from db_loader import bot, dp
import re
from dictionary_re import dictionary as dic
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from state import MainState
import sqlite3
# from sqlalchemy import create_engine, Column, Integer, String, VARCHAR, MetaData
# from sqlalchemy.orm import sessionmaker, scoped_session
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas
# from sqlalchemy.engine import URL
# from sqlalchemy.ext.asyncio import AsyncSession
# import os


poopoo = [1, 0, 0, 0, 0, 0, 0]

async def conn_start():
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS answers (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id,
                   chat_id,
                   first_message,
                   second_message,
                   third_message,
                   fourth_message,
                   status)""")
    conn.commit()




@dp.message_handler(commands=["start"])
async def cmd_start(message: types.message):
    await conn_start()
    poopoo[-1] = message.chat.id
    poopoo[-2] = message.from_user.first_name
    await bot.send_message(chat_id=message.chat.id,
                           text="Здравствуйте, это опрос из кинотеатра в который вы ходили вчера. Ответите на пару вопросов?")
    await MainState.first_message.set()


@dp.message_handler(content_types=['text'], state=MainState.first_message)
async def fist_question(message: types.message):
    count = 0
    first_message = str(message.text)
    find_interruption = re.findall(dic['interruption'], str(message))
    find_answer = re.findall(dic['first_question'], str(message))
    if find_answer:
        if len(find_answer) > 1:
            check_answer = find_answer[-1]
        else:
            check_answer = find_answer[0]
        await bot.send_message(chat_id=message.chat.id,
                               text="Рад это слышать. По десятибальной шкале насколько сильно вам понравился фильм?")
        poopoo[0] = first_message
        await MainState.first_message.set()
        await MainState.next()
    elif find_interruption:
        if len(find_interruption) > 1:
            check_answer = find_interruption[-1]
        else:
            check_answer = find_interruption[0]
        await bot.send_message(chat_id=message.chat.id, text="Очень жаль это слышать. Досвидания")
        await MainState.bot_save_end.set()
        await MainState.next()
        status = "Не пройден"
        poopoo[4] = status
    else:
        count += 1
        if count == 4:
            await bot.send_message(chat_id=message.chat.id, text="Я вас не понимаю, извините, до свидания")
            await MainState.bot_save_end.set()
            status = "Не пройден"
            poopoo[4] = status
        else:
            await bot.send_message(chat_id=message.chat.id, text="Немного не понятно, можете повторить?")
        return



@dp.message_handler(state=MainState.second_message)
async def second_question(message: types.message, state: FSMContext):
    count = 0
    async with state.proxy() as data:
        data['second_answer'] = message.text
    second_message = str(message.text)
    find_interruption = re.findall(dic['interruption'], str(message))
    find_answer = re.findall(dic['second_question'], str(message))
    if find_answer:
        if len(find_answer) > 1:
            check_answer = find_answer[-1]
        else:
            check_answer = find_answer[0]

        await bot.send_message(chat_id=message.chat.id,
                               text="По десятибальной шкале как вы оцените зал в котором вы смотрели фильм?")
        poopoo[1] = second_message
        await MainState.second_message.set()
        await MainState.next()
    elif find_interruption:
        if len(find_interruption) > 1:
            check_answer = find_interruption[-1]
        else:
            check_answer = find_interruption[0]
        await bot.send_message(chat_id=message.chat.id, text="Очень жаль это слышать. Досвидания")
        status = "Пройден частично"
        poopoo[4] = status
    else:
        count += 1
        if count == 4:
            await bot.send_message(chat_id=message.chat.id, text="Я вас не понимаю, извините, до свидания")
            await MainState.bot_save_end.set()
            status = "Пройден частично"
            poopoo[4] = status
        else:
            await bot.send_message(chat_id=message.chat.id, text="Немного не понятно, можете повторить?")
        return



@dp.message_handler(state=MainState.third_message)
async def second_question(message: types.message, state: FSMContext):
    count = 0
    async with state.proxy() as data:
        data['third_message'] = message.text
        third_message = str(message.text)
        find_interruption = re.findall(dic['interruption'], str(message))
        find_answer = re.findall(dic['second_question'], str(message))
        if find_answer:
            if len(find_answer) > 1:
                check_answer = find_answer[-1]
            else:
                check_answer = find_answer[0]
            await bot.send_message(chat_id=message.chat.id,
                           text="Если вы покупали попкорн, оцениет его вкус по десятибальной шкале?")
            poopoo[2] = third_message
            await MainState.third_message.set()
            await MainState.next()
        elif find_interruption:
            if len(find_interruption) > 1:
                check_answer = find_interruption[-1]
            else:
                check_answer = find_interruption[0]
            await bot.send_message(chat_id=message.chat.id, text="Очень жаль это слышать. Досвидания")
            status = "Пройден частично"
            poopoo[4] = status
        else:
            count += 1
            if count == 4:
                await bot.send_message(chat_id=message.chat.id, text="Я вас не понимаю, извините, до свидания")
                await MainState.bot_save_end.set()
                status = "Пройден частично"
                poopoo[4] = status
            else:
                await bot.send_message(chat_id=message.chat.id, text="Немного не понятно, можете повторить?")
            return

@dp.message_handler(state=MainState.fourth_message)
async def question_fourth(message: types.message, state: FSMContext):
    count = 0
    async with state.proxy() as data:
        data['fourth_message'] = message.text
        fourth_message = str(message.text)
        find_interruption = re.findall(dic['interruption'], str(message))
        find_answer = re.findall(dic['second_question'], str(message))
        if find_answer:
            if len(find_answer) > 1:
                check_answer = find_answer[-1]
            else:
                check_answer = find_answer[0]
            await bot.send_message(chat_id=message.chat.id,
                             text="Спасибо за ваши ответы, будем рады снова видеть вас в нашем кинотеатре!")
            poopoo[3] = fourth_message
            status = "Прошел опрос"
            poopoo[4] = status
            await MainState.fourth_message.set()
            await MainState.next()
        elif find_interruption:
            await bot.send_message(chat_id=message.chat.id, text="Очень жаль это слышать. Досвидания ")
            status = "Пройден частично"
            poopoo[4] = status
            await MainState.bot_save_end.set()
        else:
            count += 1
            if count == 4:
                await bot.send_message(chat_id=message.chat.id, text="Я вас не понимаю, извините, до свидания")
                await MainState.bot_save_end.set()
                status = "Пройден частично"
                poopoo[4] = status
            else:
                await bot.send_message(chat_id=message.chat.id, text="Немного не понятно, можете повторить?")
            return


@dp.message_handler(state=MainState.bot_save_end)
async def bot_save_end(message: types.message, state: FSMContext):
    user_id = poopoo[-2]
    chat_id = poopoo[-1]
    first_message = poopoo[0]
    second_message = poopoo[1]
    third_message = poopoo[2]
    fourth_message = poopoo[3]
    status = poopoo[4]
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO answers (user_id, chat_id, first_message, second_message, third_message, fourth_message, status) VALUES ('{user_id}','{chat_id}','{first_message}','{second_message}','{third_message}','{fourth_message}','{status}')")
    conn.commit()
    await MainState.cmd_start






if __name__ == "__main__":
    executor.start_polling(dispatcher=dp,
                           skip_updates=True)
