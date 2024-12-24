import asyncio

from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from loader import bot, dp, logger

from datetime import datetime
from keyboards import start_keyboard, generate_calendar


# await bot.send_chat_action(message.chat.id, 'Загрузка видео')
# Удаление меню команд (если имеется)
async def clear_commands(robot: Bot) -> None:
    current_commands = await robot.get_my_commands()

    if current_commands:
        await robot.set_my_commands([])
        await clear_commands(robot)


# Команда /start
@dp.message(Command('start'))
async def start(message: Message):
    await clear_commands(bot)

    today = datetime.now()
    now_year = today.year
    now_month = today.month

    await message.answer('Выберите дату:', reply_markup=start_keyboard)
    await message.answer('Милый календарь v 1.0:', reply_markup=await generate_calendar(now_year, now_month, 'rus_short'))


# Заглушка для ignore
@dp.callback_query(F.data == 'ignore')
async def ignore_callback(callback_query: CallbackQuery):
    await callback_query.answer()


# Кнопки для переключения лет
@dp.callback_query(F.data.startswith('year-'))
async def ignore_callback(callback_query: CallbackQuery):
    if callback_query.data.startswith('year-prev'):
        await callback_query.answer('Кнопка год предыдущий')
    elif callback_query.data.startswith('year-next'):
        await callback_query.answer('Кнопка год следующий')


# Кнопки для переключения месяцев
@dp.callback_query(F.data.startswith('month-'))
async def ignore_callback(callback_query: CallbackQuery):
    if callback_query.data.startswith('month-prev'):
        await callback_query.answer('Кнопка месяц предыдущий')
    elif callback_query.data.startswith('month-next'):
        await callback_query.answer('Кнопка месяц следующий')


# Запуск бота
@logger.catch
async def main():
    logger.info('Бот запущен')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


# Остановка бота
async def stop_bot() -> None:
    await bot.session.close()
    logger.info('Бот остановлен')


if __name__ == '__main__':
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        asyncio.run(stop_bot())