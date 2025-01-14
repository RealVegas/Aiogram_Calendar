import re


def parse_date_format(date_format: str) -> dict:
    """
    Функция для разбора строки формата даты.

    Параметры:
    - date_format (str): строка, представляющая формат даты, например "DD.MM.YYYY".

    Возвращает:
    - result (dict): Словарь с ключами:
        * order - порядок следования компонентов (например, {'DD': 1, 'MM': 2, 'YYYY': 3}).
        * separator - разделитель (например, "." или "-"). None, если разделителя нет.
        * valid - True, если формат валиден, False, если нет.
        * corrected_format - формат, исправленный в случае некорректных элементов (например, удалены лишние части).
    """
    # Регулярное выражение для поиска компонентов даты
    components_pattern = re.compile(r'(DD|MM|YYYY)')

    # Найдем все компоненты формата (например, DD, MM, YYYY)
    components = components_pattern.findall(date_format)

    # Если формат пустой или содержит не поддерживаемые элементы - он некорректен
    # if not components or len(components) != len(set(components)):
    #     valid = False

    day_count = components.count('DD')
    month_count = components.count('MM')
    year_count = components.count('YYYY')

    if day_count > 1 or month_count > 1 or year_count > 1:
        rev = components[::-1]

        for item in ['DD', 'MM', 'YYYY']:
            while rev.count(item) > 1:
                rev.remove(item)

        components = rev[::-1]

    # Определяем разделитель, если он есть
    # Для этого используем регулярное выражение, которое находит любой символ, не являющийся частью компонентов даты или буквой

    sym_list = ['M', 'D', 'Y']
    separator = None

    for symbol in date_format:
        if symbol not in sym_list:
            separator = symbol
            break

    # Создаем "исправленный" формат, удаляя лишние части
    if separator:
        corrected_format = separator.join(components)
    else:
        corrected_format = ''.join(components)

    valid = False if date_format != corrected_format else True

    pattern = r"(DD|MM|YYYY)"  # Паттерн ищет DD или MM

    # Созадем шаблон для strptime
    def replacer(match):
        # Словарь для замены
        replacements = {
            'DD': '%d',
            'MM': '%m',
            'YYYY': '%Y'
        }
        return replacements[match.group()]  # Возвращаем заменённое значение

    # Используем re.sub
    date_pattern = re.sub(pattern, replacer, corrected_format)

    # Возвращаем результаты
    return {
        'strptime_pattern': date_pattern,  # Строка для использования в strptime
        'separator': separator,  # Разделитель (если есть)
        'valid': valid,  # Флаг валидности формата
        'corrected_format': corrected_format  # Исправленный формат
    }


# Примеры использования функции
examples = [
    "DD.MM.YYYY",
    "YYYY-DD-MM",
    "MM/YYYY/DD",
    "DDYYYYMM",
    "YYYY.TT.MM.DD.MM",
    "YY.MM.DD",
    "DD-MM-YYYY",
    "YYYY/DD/MM/",
    "MMDDYY.YMDDYYYYMMMMDDYYYMMYY"
]

for example in examples:
    result = parse_date_format(example)
    print(f"Input format: {example}")
    print(f"Result: {result}")
    print("-" * 40)