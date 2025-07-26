# Наборы для именования дней и месяцев

import json

with open('lang.json', 'r', encoding='utf-8') as f:
    dateformat = json.load(f)

print(dateformat['ru']['day_abbr'])

# for key, val in dateformat.items():
#     print(f'{key}: {val}')