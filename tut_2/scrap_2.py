import requests
from bs4 import BeautifulSoup as BS
import json

# url = 'http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

# headers = {
    # 'Accept': '*/*',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.4.731 Yowser/2.5 Safari/537.36'
# }

# req = requests.get(url, headers=headers)

# Получаем текст нашей страницы
# src = req.text

# Сохраняем страницу в файл
# with open('tut_2\index.html', 'w') as file:
#     file.write(src)


# Теперь откроем, прочитаем и сохраним код страницы в переменную
with open('tut_2\index.html') as file:
        src = file.read()


# Создаем переменную, обращаемся к BeautifulSoup, указываем переменную с файлом и парсер lxml
soup = BS(src, 'lxml')
# По классу получаем путь до категорий
all_products_href = soup.find_all(class_='mzr-tc-group-item-href')

# Циклом пройдемся по странице и соберем названия категорий и ссылки на них. И сохраним их в словарь.
all_categories_dict = {}
for item in all_products_href:
    item_text = item.text
    item_hrefs = f"http://health-diet.ru{item.get('href')}"
    all_categories_dict[item_text] = item_hrefs

# А так же сохраним их в json файл. indent Это отступ в файле, если убрать, то получим одну строку, а ensure_ascii=False не экранирует спецсимволы и помогает при работе с кириллицей, без него будут проблемы с кодировкой
with open('tut_2/all_categoties_hrefs.json', 'w') as file:
    json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)