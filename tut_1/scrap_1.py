from cgitb import text
from bs4 import BeautifulSoup

with open('C:/Users/Eugene/Desktop/QA/scrap_tutorial/lesson1/blank/index.html') as file:
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