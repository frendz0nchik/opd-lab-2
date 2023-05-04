import datetime

import random
from aiogram import Bot, types, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import io

bot = Bot(token="6170856766:AAF-QmVVz8SFgRuy1Pi28S3lIldvFzLLgtE")
dp = Dispatcher(bot=bot, storage=MemoryStorage())

kategori = """
Выберите возрастную категорию:
"""
appointments = []
name = ''
kategoria = ''
sex = """
Укажите ваш пол:
"""
pol = ''
nomer = ''

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! я бот для записи на марафон.\n/zapis - запись на марафон\n/list - проверка записи")


@dp.message_handler(commands=['zapis'])
async def start(message: types.Message):
    await message.reply("Для продолжения напишите ваше ФИО:")

    # Добавляем состояние пользователя "ждем имя"
    await dp.current_state(user=message.from_user.id).set_state('wait_name')


@dp.message_handler(commands=['list'])
async def listok(message: types.Message):
    
    await bot.send_message(message.from_user.id,'Введите указанное ФИО')
    
    await dp.current_state(user=message.from_user.id).set_state('wait_name2')
    
@dp.message_handler(state='wait_name2')
async def process_name2(message: types.Message,state):
    name_2 = message.text
    k = 0
    with open('marathon_participants.txt', "r") as users_file:
        # Читаем все строки из файла
        lines = users_file.readlines()
        for line in lines:
            # Разбиваем строку на отдельные значения
            values = line.strip().split(",")
            if name_2 == values[0]: 
                await bot.send_message(message.from_user.id,'Вы записаны')
                k += 1
    if k == 0:
         await bot.send_message(message.from_user.id,'Вы не записаны')
    await state.finish()

        


@dp.message_handler(state='wait_name')
async def process_name(message: types.Message):
    global name
    name = message.text
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    kb.add(types.KeyboardButton('9-11 лет'))
    kb.add(types.KeyboardButton('12-13 лет'))
    kb.add(types.KeyboardButton('14-15 лет'))
    kb.add(types.KeyboardButton('16-17 лет'))
    kb.add(types.KeyboardButton('18-19 лет'))
    kb.add(types.KeyboardButton('20-22 лет'))
    kb.add(types.KeyboardButton('23 года и более'))
     
    await message.reply(text=kategori, reply_markup=kb)

    # Добавляем состояние пользователя "ждем выбор врача"
    await dp.current_state(user=message.from_user.id).set_state('wait_kategori')


@dp.message_handler(state='wait_kategori')
async def process_kategoria(message: types.Message):
    global kategoria
    kategoria = message.text
    await message.answer(f"Хорошо, вы выбрали возрастную категорию {kategoria}.")
    kb2 = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    kb2.add(types.KeyboardButton('Мужской'))
    kb2.add(types.KeyboardButton('Женский'))
    await message.reply(text=sex, reply_markup=kb2)

    # Добавляем состояние пользователя "ждем дату приема"
    await dp.current_state(user=message.from_user.id).set_state('wait_num')
    

@dp.message_handler(state='wait_num')
async def process_num(message: types.Message,state):
    global name, kategoria, pol,nomer
    pol = message.text
    nomer = random.randint(1,1000)
    appointment = name + f" - возврастная категория: {kategoria}, пол: {pol}, номер: {nomer}"
    appointments.append(appointment)
    text = f"Вы успешно записались на марафон. Запись: {appointment}"
    await message.reply(text)
    with open('marathon_participants.txt', 'a') as f:
        f.write(f'{name}, {kategoria}, {pol},{nomer}\n')
    await state.finish()


def zapusk():

    
    executor.start_polling(dp, skip_updates=True)
