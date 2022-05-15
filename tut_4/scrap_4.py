import requests
from bs4 import BeautifulSoup as BS
import json

# persons_url_list = []
# for i in range(0, 720, 20):
#     url = f"https://www.bundestag.de/ajax/filterlist/en/members/863330-863330?limit=20&noFilterSet=true&offset={i}"
    
#     q = requests.get(url)
#     result = q.content
    
#     soup = BS(result, 'lxml')
    
# Собираем ссылки на всех чиновников и сохраняем их в файл txt
#     persons = soup.find_all(class_='bt-open-in-overlay')
    
#     for person in persons:
#         person_page_url = person.get('href')
#         persons_url_list.append(person_page_url)
        
# with open('tut_4/data/person_url_list.txt', 'w') as file:
#     for line in persons_url_list:
#         file.write(f'{line}\n')

# Открываем файл со ссылками и работаем с ним
with open('tut_4/data/person_url_list.txt') as file:
    lines = [line.strip() for line in file.readlines()]
    
    data_dict = []
    count = 0
    
    for line in lines:
        if count < 10:
            q = requests.get(line)
            result = q.content
            
            soup = BS(result, 'lxml')
            
            # Найдем имена чиновников и в какой партии они состоят
            person = soup.find(class_='bt-biografie-name').find('h3').text
            
            # Так как имя и партия это одна строка и разделены они запятой то создаем список и разделяем их
            person_name_company = person.strip().split(',')
            
            person_name = person_name_company[0]
            person_company = person_name_company[1].strip()
            
            # Соберем ссылки на социальные сети
            social_networks = soup.find_all(class_='bt-link-extern')
            
            # Создадим список из этих ссылок
            social_networks_urls = []
            for item in social_networks:
                social_networks_urls.append(item.get('href'))
                
            # Теперь объеденим данные и запишем их в словарь
            data = {
                'person_name': person_name,
                'person_company': person_company,
                'social_networks': social_networks_urls
            }
            
            data_dict.append(data)
            with open('tut_4/data/data.json', 'w') as json_file:
                json.dump(data_dict, json_file, indent=4, ensure_ascii=False)
        count += 1
