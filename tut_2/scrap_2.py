import requests
from bs4 import BeautifulSoup as BS
import json
import csv
from random import randrange
from time import sleep

# url = 'http://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.4.731 Yowser/2.5 Safari/537.36'
}

# req = requests.get(url, headers=headers)

# Получаем текст нашей страницы
# src = req.text

# Сохраняем страницу в файл
# with open('tut_2\index.html', 'w') as file:
#     file.write(src)


# Теперь откроем, прочитаем и сохраним код страницы в переменную
# with open('tut_2\index.html') as file:
#         src = file.read()


# Создаем переменную, обращаемся к BeautifulSoup, указываем переменную с файлом и парсер lxml
# soup = BS(src, 'lxml')
# По классу получаем путь до категорий
# all_products_href = soup.find_all(class_='mzr-tc-group-item-href')

# Циклом пройдемся по странице и соберем названия категорий и ссылки на них. И сохраним их в словарь.
# all_categories_dict = {}
# for item in all_products_href:
#     item_text = item.text
#     item_hrefs = f"http://health-diet.ru{item.get('href')}"
#     all_categories_dict[item_text] = item_hrefs

# А так же сохраним их в json файл. indent Это отступ в файле, если убрать, то получим одну строку, а ensure_ascii=False не экранирует спецсимволы и помогает при работе с кириллицей, без него будут проблемы с кодировкой
# with open('tut_2/all_categoties_hrefs.json', 'w') as file:
#     json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)


# А теперь загрузим наш файл в переменную
with open('tut_2/all_categoties_hrefs.json') as file:
        all_categories = json.load(file)
        
# Теперь через цикл пройдемся по всем ссылкам, соберем данные о всех товаров со страницы, с описанием и химическим составом и запишем все это в файлы, где каждый файл будет называеться именем категории. При этом все проблемы, запятые и дефис заменим на нижние подчеркивание

iteration_count = int(len(all_categories)) - 1 #Количество страниц категорий
count = 0
print(f'Всего итераций: {iteration_count}')
for category_name, category_href in all_categories.items():
    # Чтобы не засорять память, создаем условие, при котором будет парситься только одна страница. Если убрать цикл, то мы соберем все страницы
    if count == 0:
        rep = [',', ' ', '-', "'"]
        for item in rep:
            if item in category_name:
                category_name = category_name.replace(item, '_')
            
        # Получаем страницу категории
        req = requests.get(url=category_href, headers=headers)
        src = req.text
        
        # Создаем файл страницы категории
        with open(f'tut_2/data/{count}_{category_name}.html', 'w') as file:
            file.write(src)
        
        # Создаем переменную которая читает созданный файл
        with open(f'tut_2/data/{count}_{category_name}.html') as file:
            src = file.read()
            
        soup = BS(src, 'lxml')
        
        # Проверка страницы на наличие таблицы с продуктами
        # Если такой класс есть на странице, то мы переходим к следующей итерации
        alert_block = soup.find(class_='uk-alert-danger')
        if alert_block is not None:
            continue
        
        # По классу, который есть только у таблицы, находим внутри класса тег tr и ищем все th
        # Собираем заголовки таблицы
        table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
        product = table_head[0].text
        calories = table_head[1].text
        proteins = table_head[2].text
        fats = table_head[3].text
        carbohydrates = table_head[4].text
        
        # Создадим таблицу с заголовками
        with open(f'tut_2/data/{count}_{category_name}.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Следующий метод добавит данные в наши заголовки, но он умеет передавать только один элемент, и чтобы передать все 5 элементов, нужно объеденить их в кортеж или список
            writer.writerow(
                (
                    product,
                    calories,
                    proteins,
                    fats,
                    carbohydrates
                )
            )
        
        
        # Теперь соберем данные из каждого столбца в наше таблице
        products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
        # И далее циклом соберем все td теги, внутри которых и содержатся названия продуктов.
        # Так же праллельно соберем все данные в json
        product_info = []
        for item in products_data:
            product_tds = item.find_all('td')
            
            title = product_tds[0].find('a').text
            calories = product_tds[1].text
            proteins = product_tds[2].text
            fats = product_tds[3].text
            carbohydrates = product_tds[4].text
            
            product_info.append(
                {
                    'Title': title,
                    'Calories': calories,
                    'Proteins': proteins,
                    'Fats': fats,
                    'Carbohydrates': carbohydrates
                }
            )
            
            # Так как мы в цикле, нам нужно добавлять значения а не создавать их, поэтому вместо флага 'w' используем 'a' - append
            with open(f'tut_2/data/{count}_{category_name}.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        title,
                        calories,
                        proteins,
                        fats,
                        carbohydrates
                    )
                )
        with open(f'tut_2/data/{count}_{category_name}.json', 'a', encoding='utf-8') as file:
            json.dump(product_info, file, indent=4, ensure_ascii=False)
        count += 1
        # Просто чтоб было видно прогресс, будем выводить какая итерация завершилась
        print(f'# Итерация {count}. {category_name} записан...')
        iteration_count -= 1
        # Чтобы после последней итерации не вывелось Осталось 0, создадим условие
        if iteration_count == 0:
            print('Работа закончена')
            break
        print(f'Осталось итераций: {iteration_count}')
        sleep(randrange(2, 4))
        