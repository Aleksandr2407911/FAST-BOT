from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, Message,
                           KeyboardButton, ReplyKeyboardMarkup, CallbackQuery)
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from user_module import list_of_admins
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from user_module import database


class AddAdmin(StatesGroup):
    WaitingForName = State()
    WaitingForText = State()
    WaitingForPicture = State()

def is_admin_filter(message: Message) -> bool:
    return message.from_user.id in list_of_admins

# Инициализируем роутер уровня модуля
router = Router()

router.message.filter(is_admin_filter)

# Создаем объект кнопок главного меню
button_1 = KeyboardButton(text='Редактировать программы')

# Создаем объект клавиатуры и добавляем кнопки главного меню
Keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1]], resize_keyboard=True)


# словарь вида {программа: [текст, фотография]} database
def compose_dc_for_orders(database):
    dc_for_orders = {}
    print(database)

    for i in database:
        dc_for_orders[f"prog_{i}"] = i
    print(dc_for_orders)
    return dc_for_orders
buttons = compose_dc_for_orders(database)


# compose_dc_for_orders(database)
async def build_inline_keyboard_for_orders(buttons):
    keyboard_list = InlineKeyboardBuilder()
    for callback, text in buttons.items():
        keyboard_list.add(InlineKeyboardButton(
            text=text, callback_data=callback))
    print('клавиатура создана')
    return keyboard_list.adjust(1).as_markup()



@router.message(Command(commands= ['start_admin']))
async def process_start_command(message: Message):
    print('хэндлер перехода в меню администратора сработал')
    await message.answer(text='Вы перешли в меню редактирования',
                         reply_markup=Keyboard)



@router.message(F.text == 'Редактировать программы')
async def process_start_command(message: Message):
    print('хэндлер перехода в меню администратора сработал')
    await message.answer(text='Вы перешли в меню администратора',
                         reply_markup=await build_inline_keyboard_for_orders(buttons))


# Клавиатура для редактора
button_change_name = InlineKeyboardButton(text='Изменить название программы', callback_data='change_name')
button_change_text = InlineKeyboardButton(text='Изменить текст ответа', callback_data='change_text')
button_change_picture = InlineKeyboardButton(text='Изменить картинку', callback_data='change_picture')

keyboard_cd_order = InlineKeyboardMarkup(inline_keyboard=[[button_change_name],
                                                          [button_change_text],
                                                          [button_change_picture]])

# Возвращает клавиатуру редактора
@router.callback_query(lambda callback: callback.data.startswith('prog_'))
async def reply_to_order(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    await state.update_data(data_product=callback.data)
    await callback.answer()
    await callback.message.edit_text(text='Ответить на заказ', reply_markup=keyboard_cd_order)

# Ловит имя программы и добавляет ее в database
@router.callback_query(F.data == "change_name")
async def reply_to_changene_name(callback: CallbackQuery, state: FSMContext):
    #await state.update_data(data_product=callback.data)
    await callback.answer(show_alert=True)
    await callback.message.edit_text(text='Введите новое имя программы')
    await state.set_state(AddAdmin.WaitingForName)

# Ловит имя  текс и добавляет его в database
@router.callback_query(F.data == "change_text")
async def reply_to_change_text(callback: CallbackQuery, state: FSMContext):
    #await state.update_data(data_product=callback.data)
    await callback.answer(show_alert=True)
    await callback.message.edit_text(text='Введите новый текст программы')
    await state.set_state(AddAdmin.WaitingForText)

# Ловит картинку и добавляет ее в database
@router.callback_query(F.data == "change_picture")
async def reply_to_change_picture(callback: CallbackQuery, state: FSMContext):
    #await state.update_data(data_product=callback.data)
    await callback.answer(show_alert=True)
    await callback.message.edit_text(text='Отправте новую картинку программы')
    await state.set_state(AddAdmin.WaitingForPicture)


'''
@router.message(Command(commands= ['admin']))
async def process_start_command(message: Message, state: FSMContext):
    await message.answer(text='Введите пароль')
    await state.set_state(AddAdmin.WaitingForPassword)'''

# Ввод name
@router.message(AddAdmin.WaitingForName)
async def process_password_input(message: Message, state: FSMContext):
    global buttons
    # Ловит сообщение
    entered = message.text.strip()
    data = await state.get_data()
    # Получаем сохраненное имя продукта из состояния
    name = data.get('data_product')[5:]
    print(name)
    database[entered] = database.pop(name)
    buttons = compose_dc_for_orders(database)
    print(buttons)
    print(database)

    # Сброс состояния FSM
    await state.clear()
    await message.answer(text= str(database))

# Ввод text
@router.message(AddAdmin.WaitingForText)
async def process_password_input(message: Message, state: FSMContext):
    global buttons
    # Ловит сообщение
    entered = message.text.strip()
    data = await state.get_data()
    # Получаем сохраненное имя продукта из состояния
    name = data.get('data_product')[5:]
    database[name][0] = entered
    buttons = compose_dc_for_orders(database)

    # Сброс состояния FSM
    await state.clear()
    await message.answer(text= str(database))


# Ввод picture
@router.message(AddAdmin.WaitingForPicture)
async def process_password_input(message: Message, state: FSMContext):
    global buttons
    # Ловит сообщение
    #entered = message.text.strip()
    photo = message.photo[-1].file_id
    print(photo)
    data = await state.get_data()
    # Получаем сохраненное имя продукта из состояния
    name = data.get('data_product')[5:]
    database[name][1] = photo
    buttons = compose_dc_for_orders(database)

    # Сброс состояния FSM
    await state.clear()
    await message.answer(text= str(database))