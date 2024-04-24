import logging
import asyncio
from aiogram import Bot, Dispatcher
import user_module
import admin_module
from user_module import list_of_admins

async def clear_admin_list():
    while True:
        await asyncio.sleep(600)  # Подождать 10 минут
        list_of_admins.clear()  # Очистить список администраторов

#функция конфигурирования и запуска бота
async def main():
    
    await clear_admin_list()
    
    #регистрируем бота и диспетчер
    bot = Bot(token= '6982700202:AAGziEKEE79FgTdwtUjebPsfUbVcMV_w_p0')
    dp = Dispatcher()

    #регистрируем роутеры в диспетчер
    #dp.include_router(admin_module.router)
    dp.include_router(user_module.router)

    #пропускаем накопившиемя апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('Запуск прошел успешно')
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
