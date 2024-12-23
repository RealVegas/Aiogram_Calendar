import asyncio
from datetime import datetime

from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from loader import bot, dp, logger

from keyboards import start_keyboard
from keyboards import combo_keyboard, new_keyboard


# await bot.send_chat_action(message.chat.id, 'Загрузка видео')

# Удаление меню команд (если имеется)
async def clear_commands(robot: Bot) -> None:
    current_commands = await robot.get_my_commands()

    if current_commands:
        await robot.set_my_commands([])
        await clear_commands(robot)


# Словарь для лет и месяцев
year_dict = {
                'prev_year': '<', 'Y_none': str(datetime.now().year), 'next_year': '>',
                'prev_month': '<', 'М_none': str(datetime.now().month), 'next_month': '>'
}


@dp.message(Command('start'))
async def bot_start(message: Message):
    await clear_commands(bot)
    await message.delete()
    await message.answer('Привет! Добро пожаловать в календарь', reply_markup=start_keyboard)
    await message.answer('Календарь v1.0', reply_markup=combo_keyboard)


# Переключение лет
@dp.callback_query(F.data.endwith('year'))
async def change_year(callback: CallbackQuery):
    old_year = year_dict['Y_none']

    if callback.data == 'prev_year':
        prev_year = int(year_dict['Y_none']) - 1
        if prev_year >= datetime.now().year:
            year_dict['Y_none'] = str(prev_year)

    elif callback.data == 'next_year':
        next_year = int(year_dict['Y_none']) + 1
        if next_year <= datetime.now().year + 10:
            year_dict['Y_none'] = str(next_year)

    if year_dict['Y_none'] != old_year:
        await callback.message.edit_text('Календарь v1.0', reply_markup=combo_keyboard)

    await callback.answer()


# Переключение месяцев
@dp.callback_query(F.data.endwith('month'))
async def change_year(callback: CallbackQuery):
    old_month = year_dict['М_none']

    if callback.data == 'prev_month':
        prev_month = int(year_dict['М_none']) - 1
        if prev_month >= 1:
            year_dict['М_none'] = str(prev_month)

    elif callback.data == 'next_month':
        next_month = int(year_dict['М_none']) + 1
        if next_month <= 12:
            year_dict['М_none'] = str(next_month)

    if year_dict['М_none'] != old_month:
        await callback.message.edit_text('Календарь v1.0', reply_markup=await combo_keyboard(year_dict))

    await callback.answer()


# Запуск  и остановка бота
@logger.catch
async def main():
    logger.info('Бот запущен')
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


async def stop_bot() -> None:
    await bot.session.close()
    logger.info('Бот остановлен')


if __name__ == '__main__':
    today = datetime.today()
    curr_year = today.year
    curr_month = today.month


    try:

        asyncio.run(main())
        #asyncio.run(month_calend(curr_year, curr_month))

    except KeyboardInterrupt:
        asyncio.run(stop_bot())