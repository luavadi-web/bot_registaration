import asyncio
import os
import sqlite3
import openpyxl
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart  # Исправлено: правильный импорт
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
# ВАЖНО: Замените на ваш НОВЫЙ токен, полученный через @BotFather (Revoke)
save_dir = r'saved_photos2'
save_users = r'saved_users_photo'
EXCEL_FILE_BALL = r'Рейтинг 2,0 в цифрах.xlsx'
SHEET_NAME_BALL = r'с цифрами'
workbook = openpyxl.load_workbook(EXCEL_FILE_BALL)
sheet = workbook[SHEET_NAME_BALL]
conn = sqlite3.connect('Userslog2.sql')
cur = conn.cursor()
cur.execute('CREATE  TABLE IF NOT EXISTS USERS_AND_POINTS (id INTEGER PRIMARY KEY AUTOINCREMENT, name , phone_number ,pers_number , TGiD, sex ,date , seat , user_photo_path ,SPORT ,SOCIAL ,SCIENCE,EDUCATION , ALLBALL , PLACE, ADMIN)')
cur.execute('CREATE  TABLE IF NOT EXISTS log (timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, name , TGiD, COMPETITION ,photo_path)')
cur.execute('CREATE  TABLE IF NOT EXISTS VARIABLE (id INTEGER PRIMARY KEY AUTOINCREMENT,name , phone_number , pers_number ,sex ,date , seat ,user_photo_path , ACHIVEMENT , ACHIVEMENT1 , ACHIVEMENT2 , ACHIVEMENT3 ,ACHIVEMENT4 , ACHIVEMENT5 , GREATACH , GREATACH1 , TGID , pref , achlog ,sportvalue , artvalue , sciencevalue , educationvalue , sportvalue1 , artvalue1 , sciencevalue1 , educationvalue1 )')
cur.execute('CREATE TABLE IF NOT EXISTS navigation_stack (id INTEGER PRIMARY KEY AUTOINCREMENT,TGID INTEGER,state TEXT,timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
conn.commit()
cur.close()
conn.close()
TOKEN = '8757484101:AAH15G06lK5zPvrjYQBSYQCf3PU-gAyWmjY'

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: types.Message):
    buttons = [[KeyboardButton(text='Регистрация',web_app=WebAppInfo(url='https://google.com'))],[KeyboardButton(text='Рейтинг участников',web_app=WebAppInfo(url='https://google.com'))]]
    markup = ReplyKeyboardMarkup(keyboard=buttons,resize_keyboard=True,input_field_placeholder="Нажмите на кнопку регистрации")
    user_name = message.from_user.first_name
    await message.answer(f'Привет, {user_name}! Я чат-бот 😇 Лиги будущего Гомельэнерго.Я буду оповещать о мероприятиях проводимых лигой будущего, и РУП Гомельэнерго. А еще ты сможешь зарегистрировать свои достижения в различных сферах получая за это баллы) ',reply_markup=markup)


async def main():
    print("Бот запущен и готов к работе...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен пользователем")
    except Exception as e:
        print(f"Произошла ошибка: {e}")