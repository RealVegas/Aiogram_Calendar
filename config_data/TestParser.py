# import sys
import re
from datetime import datetime


def parse_date_format(date_format: str) -> tuple[bool, str, str | None]:
    """
    Функция для разбора строки формата даты.

    Параметры:
    * date_format (str): строка, представляющая формат даты

    Возвращает:
    * p_format - строка для использования в datetime.strptime.

    """
    date_blocks: list[str] = re.findall(r'(DD|MM|YYYY)', date_format)

    if not date_blocks:
        return False, date_format, None

    # Подсчет дубликатов
    blocks_count: list[int] = [date_blocks.count('DD'), date_blocks.count('MM'), date_blocks.count('YYYY')]

    # Удаление дубликатов (если они есть)
    if any(num > 1 for num in blocks_count):
        rev_blocks: list[str] = date_blocks[::-1]

        for item in ['DD', 'MM', 'YYYY']:
            while rev_blocks.count(item) > 1:
                rev_blocks.remove(item)

        date_blocks: list[str] = rev_blocks[::-1]

    # Поиск разделителя
    restricted: list[str] = ['M', 'D', 'Y']
    separator: str = ''

    for char in date_format:
        if char not in restricted:
            separator: str = char
            break

    # Создаем "исправленный" формат, удаляя лишние части
    if separator:
        cor_format: str = separator.join(date_blocks)
    else:
        cor_format: str = ''.join(date_blocks)

    # Проверка валидности date_format
    valid: bool = True if date_format == cor_format else False

    # Создание строки для использования в datetime.strptime
    p_format: str = cor_format.replace('DD', '%d').replace('MM', '%m').replace('YYYY', '%Y')

    # Возвращаем результаты
    return valid, cor_format, p_format


def check_start(start_date) -> tuple[str, bool, bool] | None:
    start_decision: bool = False
    conform_check: bool = False

    start_body: list[str] = re.findall(r'\b(now)\b', start_date)
    start_ending: str = re.sub(r'(now)', '', start_date)

    print(start_body)
    out_date = start_date

    if start_body == ['now']:
        if start_ending == '':
            start_decision: bool = True
        else:
            out_date = 'now'
            start_decision: bool = False

    else:
        try:
            datetime.strptime(start_date, '%d-%m-%Y')
            conform_check: bool = True
            start_decision: bool = True

        except ValueError:
            start_decision: bool = False
            out_date = datetime.now().strftime('%d-%m-%Y')

    # if not start_decision:
    #     sys.exit('Начальная дата не указана, либо указана неверно')

    return out_date, conform_check, start_decision


# Примеры использования функции
examples = [
    'now+2',
    '24.10.2025'
]
for example in examples:
    result = check_start(example)
    print(f"Input format: {example}")
    print(f"Result: {result}")
    print("-" * 40)