import logging
import asyncio
from aiogram import Bot, Dispatcher
import user_module
import admin_module

#функция конфигурирования и запуска бота
async def main():

    #регистрируем бота и диспетчер
    bot = Bot(token= '6959535259:AAG9_n3clewzUgapOgGAcejPDRpjQ0f_C7s')
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
