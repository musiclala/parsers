import json

from grab import Grab
from fake_useragent import UserAgent
import datetime
import pandas as pd
import pycurl


def get_info(g, url):
    g.go(url)
    list_category = [i.get('href') for i in g.doc.tree.xpath('//a[@class="d-block h-100"]')]

    result = []
    count = 0
    for url_detail in list_category:
        count = 0
        get_url_test = url_detail[url_detail.rindex('/')+1:]
        url_test = f'https://api.opti-com.ru/v1.1/catalog/products?limit=1499&offset=0&order=state:asc&catalog[]={get_url_test}'

        g.go(url_test, log_file='json.json')
        with open('json.json') as file:
            data = json.load(file)

        try:
            for item in data['products']:
                added = datetime.datetime.now().strftime("%Y-%m-%d")
                updated = datetime.datetime.now().strftime("%Y-%m-%d")

                count += 1

                g.go('https://www.opti-com.ru/catalog/product/' + str(item['id']))
                brand = g.doc.tree.xpath('//a[@class="a black hover-green fz-tbx fz-lg-tb"]/span/text()')
                category = g.doc.tree.xpath('//ul[@class="list-bread-crumb lh-1em"]/li/a/text()')

                result.append({
                    'SKU': item['article'],
                    'Name': item['title'],
                    'Brand':  '' if not brand else brand[0],
                    'category1': ' ' if len(category) <= 1 else category[0],
                    'category2': ' ' if len(category) <= 2 else category[1],
                    'category3': ' ' if len(category) <= 3 else category[2],
                    'category4': ' ' if len(category) <= 4 else category[3],
                    'category5': ' ' if len(category) <= 5 else category[4],
                    'price_old': '' if not item['oldsaleprice'] else item['oldsaleprice'],
                    'price':  '' if not item['openprice'] else item['openprice'],
                    'price_unit': ' ' if not item['units'] else item['units'][0]['title'] + '.',
                    'available': 'N' if not item['units'] else 'Y',
                    'added': added,
                    'updated': updated,
                    'url': 'https://www.opti-com.ru/catalog/product/' + str(item['id']),
                    'image_url': 'https://files.opti-com.ru//products/medium/' + str(item['thumb']),
                })
        except Exception as ex:
            continue
    print(count)
    return result


if __name__ == '__main__':
    g = Grab()
    g.setup(user_agent=UserAgent().chrome)
    g.setup(proxy='', proxy_type='http', connect_timeout=5, timeout=5)
    url = 'https://www.opti-com.ru'

    result = get_info(g, url)

    try:
        df = pd.DataFrame(
            {
                'SKU': [result[x]['SKU'] for x in range(0, len(result))],
                'Name': [result[x]['Name'] for x in range(0, len(result))],
                'Brand': [result[x]['Brand'] for x in range(0, len(result))],
                'category1': [result[x]['category1'] for x in range(0, len(result))],
                'category2': [result[x]['category2'] for x in range(0, len(result))],
                'category3': [result[x]['category3'] for x in range(0, len(result))],
                'category4': [result[x]['category4'] for x in range(0, len(result))],
                'category5': [result[x]['category5'] for x in range(0, len(result))],
                'price_old': [result[x]['price_old'] for x in range(0, len(result))],
                'price': [result[x]['price'] for x in range(0, len(result))],
                'price_unit': [result[x]['price_unit'] for x in range(0, len(result))],
                'available': [result[x]['available'] for x in range(0, len(result))],
                'added': [result[x]['added'] for x in range(0, len(result))],
                'updated': [result[x]['updated'] for x in range(0, len(result))],
                'url': [result[x]['url'] for x in range(0, len(result))],
                'image_url': [result[x]['image_url'] for x in range(0, len(result))],
            })
        df.to_excel('name.xlsx')
    except Exception as ex:
        print(ex)





