from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, Message,
                           KeyboardButton, ReplyKeyboardMarkup, CallbackQuery, FSInputFile)
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext


class AddAdmin(StatesGroup):
    WaitingForPassword = State()


# инициализируем роутер уровня модуля
router = Router()

list_of_admins = []
s = '''fsalfkskkkkkkkkkkksksdaklsdkaldklsakdlmaskfnkgndjgnkgdsnkngds
aglmd;lgmkdsgknadgklndslkagnlkadgnkldsamkgnmdaklgnlkadsgnkladgklmdagkdakgmakg
dsgdg
sGdgglmsKGMKGMSLKGDMKDSMLFMSfm;MF;LSMLDFSMDSF
FD
DFmfdsm;kds;FM;lfdm;ldsmfdsmf;mfsd;

as;lfmksamfksafkafsksafksamfk;lfsaml;sfmlfsmkasfkifnkfneiniwngipgm;aekmf;km
a
skasflkdmasdlmads
sad
amsdlkasflkflksmfalk'''
database = {'1 программа': [s,
                            r'c:\Users\Vladimir\Downloads\kartinki-pyure-11.jpeg'], '2 программа': ['2 программа ...', r'c:\Users\Vladimir\Downloads\kartinki-pyure-11.jpeg']}


async def build_inline_keyboard_for_products(database):
    keyboard_list = InlineKeyboardBuilder()
    for text in database:
        keyboard_list.add(InlineKeyboardButton(
            text=text, callback_data=f'program_{text}'))
    return keyboard_list.adjust(1).as_markup()

# Создаем объект кнопок главного меню
button_1 = KeyboardButton(text='Программы')
button_2 = KeyboardButton(text='Участвовать')
button_3 = KeyboardButton(text='Социальные сети')

# Создаем объект клавиатуры и добавляем кнопки главного меню
Keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1], [button_2], [button_3]], resize_keyboard=True)


button_vk = InlineKeyboardButton(text='VK', url='https://vk.com')
button_tg = InlineKeyboardButton(text='Telegram', url='https://telegram.org')
keyboard_social = InlineKeyboardMarkup(
    inline_keyboard=[[button_vk, button_tg]])

button_takepart = InlineKeyboardButton(
    text='Перейти на сайт', url='https://www.google.com')
keyboard_takepart = InlineKeyboardMarkup(inline_keyboard=[[button_takepart]])


@router.message(Command(commands=['start', 'menu']))
async def process_start_command(message: Message):
    await message.answer_photo(caption='Hi', photo=FSInputFile(r'c:\Users\Vladimir\Downloads\kartinki-pyure-11.jpeg'), reply_markup=Keyboard)


@router.message(F.text == 'Программы')
async def process_menu_command(message: Message):
    await message.answer(text='Список программ', reply_markup=await build_inline_keyboard_for_products(database))


@router.message(F.text == 'Участвовать')
async def process_menu_command(message: Message):
    await message.answer(text='Для участия перейдите нажмите кнопку', reply_markup=keyboard_takepart)


@router.message(F.text == 'Социальные сети')
async def process_menu_command(message: Message):
    await message.answer(text='Социальные сети', reply_markup=keyboard_social)


@router.message(Command(commands=['admin']))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text='Введите пароль')
    await state.set_state(AddAdmin.WaitingForPassword)


@router.message(AddAdmin.WaitingForPassword)
async def process_password_input(message: Message, state: FSMContext):
    # Здесь вы можете сравнить введенный пароль с ожидаемым
    expected_password = '1234'
    entered_password = message.text.strip()

    if entered_password == expected_password:
        # Добавление пользователя в список администраторов
        # Например:
        user_id = message.from_user.id
        list_of_admins.append(user_id)

        await message.answer(text='Вы добавлены в список администраторов. Нажмите /start_admin')
    else:
        await message.answer(text='Неверный пароль. Для новой попытки /admin')

    # Сброс состояния FSM
    await state.clear()


@router.callback_query(lambda callback: callback.data.startswith("program_"))
async def return_to_category(callback: CallbackQuery):
    await callback.answer()  # Убирает мигание инлайн кнопки
    s = callback.data.strip("program_")
    data = database[s]

    if '.' in data[1]:
        photo = FSInputFile(data[1])
    else:
        photo = data[1]

    await callback.message.answer_photo(caption=data[0], photo=photo)
