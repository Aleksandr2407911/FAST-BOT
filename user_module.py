from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, Message,
                           KeyboardButton, ReplyKeyboardMarkup, CallbackQuery)
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder


# инициализируем роутер уровня модуля
router = Router()

# Создаем объект кнопок главного меню
button_1 = KeyboardButton(text='Программы')
button_2 = KeyboardButton(text='Участвовать')
button_3 = KeyboardButton(text='Социальные сети')

# Создаем объект клавиатуры и добавляем кнопки главного меню
Keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1], [button_2], [button_3]], resize_keyboard=True)