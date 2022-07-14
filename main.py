import csv

import requests
from bs4 import BeautifulSoup
inport csv

URL = 'https://auto.ru/cars/wanderer/all/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.0.1841 Yowser/2.5 Safari/537.36' , 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}
HOST = 'https://auto.ru'

def get_html(url,params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def get_pages_count(html):
    pagination = []
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('a', class_='ListingPagination__page')
    if pagination:
        return int(pagination[-1].get_text(strip=True))
    else:
        return 1

def get_content (html):
    soup = BeautifulSoup (html, 'html.parser')
    items = soup.find_all('div', class_ ='ListingItem')

    cars = []
    for item in items:
        cars.append({
            'title' : item.find('a' , class_='Link ListingItemTitle__link').get_text(strip=True),
            'link': item.find('a', class_='Link ListingItemTitle__link').get('href'),
            'stoim': item.find('div', class_='ListingItemPrice__content').get_text(strip=True),
            'probeg': item.find('div', class_='ListingItem__kmAge').get_text(strip=True),
            'gorod': item.find('span', class_='MetroListPlace__regionName MetroListPlace_nbsp').get_text(strip=True),

            })
    return cars

def save_file(items, path):
    with oper(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Марка', 'Ссылка', 'Цена', 'Пробег', 'Город'])
        for item in items:
            writer.writerow(item['title'],item['link'],item['stoim'],item['probeg'],item['gorod'])

def parse():
    html = get_html(URL)
    html.encoding = 'utf-8'
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print ('Парсинг страницы '+ str(page) + ' из' + str(pages_count) + ' pages_count ...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
            #cars = get_content(html.text)
        print("Получено " + str(len(cars)) + " автомобилей" )
    else:
        print("Введенный адрес недоступен")

parse()