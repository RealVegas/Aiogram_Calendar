import asyncio

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from loader import bot, dp, logger

from keyboards import start_keyboard


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
    await message.answer('Выберите дату:', reply_markup=start_keyboard)
    await message.answer('Милый календарь v 1.0:', reply_markup=generate_calendar)


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