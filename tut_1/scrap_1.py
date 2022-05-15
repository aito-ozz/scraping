from cgitb import text
from bs4 import BeautifulSoup
import re

with open('tut_1\index.html') as file:
    src = file.read()
    
soup = BeautifulSoup(src, 'lxml')


##################### Получение текста из тега
# title = soup.title
# print(title.text)
# print(title.string)


##################### Соберет данные из первого попавшегося тега <tag name>
# page_h1 = soup.find('h1')

##################### Соберет данные из всех подобных тегов
# page_all_h1 = soup.find('h1')
# Которые можем перебрать в цикле
# for item in page_all_h1:
    # print(item.text)
    
##################### Чтобы достучаться до класса, первым аргументом указываем тег(хотя это необязательно, если мы уверенны что данный класс единственный на странице), а следующим класс. Но так как class это ключевое зарезервированное имя, то нужно дописать нижний слеш _. И таким образом мы получим блок кода целиком.
# user_name = soup.find('div', class_='user__name')
# Но так как этот блок кода все еще объект soup, то можем применить метод .text и вытащить желаемое имя. И так как это уже строка, добавляем метод strip и удаляем лишние пробелы в начале и конце строки
# print(user_name.text.strip())

##################### Мы можем и пойти вглубь и применить метод find снова и найти нужный тег
# user_name = soup.find('div', class_='user__name').find('span').text

##################### Вторым вариантом поиска по атрибуту является словарь, где в ключе мы указываем сам атрибут, а в значении его значение
# user_name = soup.find('div', {'class' : 'user__name'}).text
# Так же можем задавать сразу несколько атрибутов, например
# user_name = soup.find('div', {'class' : 'user__name', 'id' : 'user'}).text

# Соберем все теги span в теге div с атрибутом class='user__info'
# find_all_span_in_user_info = soup.find(class_='user__info').find_all('span')
# Пробежимся по списку и напечатаем текст внутри каждого блока span
# for item in find_all_span_in_user_info:
    # print(item.text)
# Та как это обычный список, то мы можем обращаться к его элементам по индексу
# print(find_all_span_in_user_info[1].text)

##################### Спарсим ссылки на соц сети с нашего файла
# social_links = soup.find(class_='social__networks').find('ul').find_all('a')
# Можем не бежать в глубину, мы может просто собрать все ссылки со страницы
# all_a = soup.find_all('a')
# Чтобы вытащить ссылки из тегов, мы применим снова цикл
# for item in all_a:
#     item_text = item.text
#     item_url = item.get('href')
#     print(f'{item_text} : {item_url}')


##################### еще способы ходить по DOM дереву
# Методы .find_parent() и .find_parents()
# post_div = soup.find(class_='post__text').find_parent()
# post_div = soup.find(class_='post__text').find_parent('div', 'user__post')
# post_div = soup.find(class_='post__text').find_parents()

# .next_element .previous_element
# Так как перенос строки это тоже елемент DOM, то он и выведет нам его в этом случае
# next_el = soup.find(class_='post__title').next_element 
# Чтобы исправить этот момент, мы можем еще раз вызвать .next_element
# next_el = soup.find(class_='post__title').next_element.next_element.text

# Но еще есть похожий метод, который сразу вернет нам следующий элемент, find_next()
# next_el = soup.find(class_='post__title').find_next().text
# Точно так же работает и previous_element() только снизу вверх

# .find_next_sibling() .find_previous_sibling() Они возвращают следующий и предыдущий элемент внутри искомого тега
# next_sib = soup.find(class_='post__title').find_next_sibling()
# next_sib = soup.find(class_='post__text').find_previous_sibling()
# Комбинировать методы можем как угодно, например
# next_sib = soup.find(class_='post__date').find_previous_sibling().find_next().text

# Соберем все ссылки в конце документа
# links = soup.find(class_='some__links').find_all('a')
# for link in links:
    # link_href_attr = link.get('href')
    # Парсить содержимое можно не только с помощью get, но и просто обращаясь к нужному атрибуту
    # link_href_attr = link.['href']
    # link_data_attr = link.get('data-attr')
    # print(f'{link_data_attr} : {link_href_attr}')
# Можно искать элементы передавая в параметры текст. Сам soup ищет только по полному содержимому текста в теге.
# Но это можно исправить следующим способом. Можем использовать модуль регулярных выражений re, который имеет модуль compile (.re.compale()). Но он чувствителен к регистру, и для него слова одежда и Одежда будут разными
find_a_by_text = soup.find('a', text=re.compile('одежда'))
# Но можно указать поискать в обоих регистрах и найти все теги где есть текст одежда
find_all_clothes = soup.find_all(text=re.compile('([Оо]дежда)'))
print(find_all_clothes)