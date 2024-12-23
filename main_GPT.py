import asyncio

from aiogram import F
from aiogram.types import InlineKeyboardButton, CallbackQuery, Message  # , InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
# from aiogram.utils import executor
from datetime import datetime  # , timedelta
import calendar


# ОТСЮДА НАДО ВЗЯТЬ calendar




from loader import bot, dp, logger

@logger.catch

async def generate_calendar(year, month):
    # Первый ряд: выбор года и месяца
    cal_markup = InlineKeyboardBuilder()

    cal_text = ['<', f'{year}', '>', '<', f'{datetime(year, month, 1).strftime("%B")}', '>']
    cal_back = [f'year_dec_{year}_{month}', 'ignore', f'year_inc_{year}_{month}', f'month_dec_{year}_{month}', 'ignore', f'month_inc_{year}_{month}']

    for c_text, c_back in zip(cal_text, cal_back):

        cal_markup.add(InlineKeyboardButton(text=c_text, callback_data=c_back))

    # Третий ряд: дни недели
    week_days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    for name_day in week_days:
        cal_markup.add(InlineKeyboardButton(text=name_day, callback_data='ignore'))

    return cal_markup.adjust(3).as_markup()

    # Числа месяца
    # month_calendar = calendar.monthcalendar(year, month)
    # for week in month_calendar:
    #     for num_day in week:
    #         if num_day == 0:
    #             calendar_markup.add(InlineKeyboardButton(text=' ', callback_data='ignore'))
    #
    #         else:
    #             calendar_markup.add(InlineKeyboardButton(text=str(num_day), callback_data=f'day_{year}_{month}_{num_day}'))



        # calendar_markup.row(row)



    # print('числа месяца готовы')

@dp.message(Command('start'))
async def bot_start(message: Message):
    today = datetime.today()
    await message.answer('Выберите дату:', reply_markup=await generate_calendar(today.year, today.month))





# @dp.message(Command('start'))
# @logger.catch
# async def start(message: types.Message):
#     today = datetime.today()
#     await message.answer('Выберите дату:', reply_markup=await generate_calendar(today.year, today.month))


@dp.callback_query(F.text.startswith('ignore'))
async def ignore_callback(callback_query: CallbackQuery):
    await callback_query.answer()


@dp.callback_query(F.text.startswith('year_'))
async def process_year_change(callback_query: CallbackQuery):
    _, action, year, month = callback_query.data.split('_')
    year, month = int(year), int(month)

    if action == 'dec':
        year -= 1
    elif action == 'inc':
        year += 1

    await callback_query.message.edit_reply_markup(generate_calendar(year, month))


@dp.callback_query(F.text.startswith('month_'))
async def process_month_change(callback_query: CallbackQuery):
    _, action, year, month = callback_query.data.split('_')
    year, month = int(year), int(month)

    if action == 'dec':
        month -= 1
        if month < 1:
            month = 12
            year -= 1
    elif action == 'inc':
        month += 1
        if month > 12:
            month = 1
            year += 1

    await callback_query.message.edit_reply_markup(generate_calendar(year, month))


@dp.callback_query(F.text.startswith('day_'))
async def process_day_selection(callback_query: CallbackQuery):
    _, year, month, day = callback_query.data.split('_')
    selected_date = datetime(int(year), int(month), int(day))
    await callback_query.message.reply(f'Вы выбрали дату: {selected_date.strftime("%d.%m.%Y")}')


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
    # executor.start_polling(dp, skip_updates=True)
    try:
        asyncio.run(main())

    except KeyboardInterrupt:
        asyncio.run(stop_bot())