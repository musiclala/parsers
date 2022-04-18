from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import pandas as pd
import datetime

import urllib3


# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
URL = 'https://www.artplast.ru'


headers = {
    'user-agent': UserAgent().chrome,
}

proxies = {

}

response = requests.get(url=URL, headers=headers, proxies=proxies, verify=False)
soup = BeautifulSoup(response.text, 'lxml')

# with open('index.html', 'w', encoding='utf-8') as file:
#     file.write(response.text)

# получаем список ссылок
list_url = []
aside = soup.select('aside.sidebar > ul.mega-menu > li')
for i in aside:
    list_url.append(i.find('a')['href'])


list_url_all_card = []
for item in list_url[2:-2]:  # обрезаем акции и что-то еще.
    url_all_page = URL + item + '?SHOWALL_1=1'
    resp = requests.get(url=url_all_page, headers=headers, proxies=proxies, verify=False)
    soup_detail = BeautifulSoup(resp.text, 'lxml')

    list_all_url = soup_detail.find_all('div', 'product-item-home')

    for i in list_all_url:
        list_url_all_card.append(i.find('a')['href'])


result = []
for item in list_url_all_card[::-1]:
    url_detail_card = URL + item
    resp = requests.get(url=url_detail_card, headers=headers, proxies=proxies, verify=False)
    soup_detail = BeautifulSoup(resp.text, 'lxml')

    sku = ''.join([i.find('span').text for i in soup_detail.select('div.product-detail-top__articl')])
    name_detail = soup_detail.find('h1', class_='page-title').text

    path = [i.find('span').text for i in soup_detail.select('div.breadcrumbs li')][:-1]

    # price_old = я у них не нашел на сайте.

    price = soup_detail.find('span', class_='product-prices__price price-cell').text

    # два варианта, не знаю какой правильный
    price_unit = soup_detail.find('span', class_='minimal-order-title').text.strip()
    # price_unit_test1 = price_unit[19:]  # '1100 шт.' Потому что цена идет не за штуку, а за 1100 штук
    price_unit_test2 = price_unit[price_unit.rfind(' '):].strip()  # или просто 'шт.'

    available = ''.join([i.find('span', class_='in-nalichie__toggle').text.strip()
                 for i in soup_detail.select('div.product-detail-right__top')])

    available_result = ''
    if 'скоро в наличии' in available:
        available_result = 'N'
    elif 'в наличии' in available:
        available_result = 'Y'
    else:
        available_result = 'N'

    added = datetime.datetime.now().strftime("%Y-%m-%d")
    updated = datetime.datetime.now().strftime("%Y-%m-%d")

    url_card = url_detail_card

    image_url = ''.join([i.find('a', class_='fancybox_image')['href']
                    for i in soup_detail.select('div.item.product-detail-left__imgmain')][1:2])

    result.append({

            'SKU': sku,
            'Name': name_detail,
            'category1': ' ' if len(path) <= 1 else path[0],
            'category2': ' ' if len(path) <= 2 else path[1],
            'category3': ' ' if len(path) <= 3 else path[2],
            'category4': ' ' if len(path) <= 4 else path[3],
            'category5': ' ' if len(path) <= 5 else path[4],
            'price': price,
            'price_unit': price_unit_test2,
            'available': available_result,
            'added': added,
            'updated': updated,
            'url': url_card,
            'image_url': image_url
    })

df = pd.DataFrame(
    {
        'SKU': [result[x]['SKU'] for x in range(0, len(result))],
        'Name': [result[x]['Name'] for x in range(0, len(result))],
        'category1': [result[x]['category1'] for x in range(0, len(result))],
        'category2': [result[x]['category2'] for x in range(0, len(result))],
        'category3': [result[x]['category3'] for x in range(0, len(result))],
        'category4': [result[x]['category4'] for x in range(0, len(result))],
        'category5': [result[x]['category5'] for x in range(0, len(result))],
        'price': [result[x]['price'] for x in range(0, len(result))],
        'price_unit': [result[x]['price_unit'] for x in range(0, len(result))],
        'available': [result[x]['available'] for x in range(0, len(result))],
        'added': [result[x]['added'] for x in range(0, len(result))],
        'updated': [result[x]['updated'] for x in range(0, len(result))],
        'url': [result[x]['url'] for x in range(0, len(result))],
        'image_url': [result[x]['image_url'] for x in range(0, len(result))],
    })

df.to_excel('name.xlsx')









