import requests
import pandas as pd

headers = {

}


def get_data_file(headers):
    offset = 0
    result = []
    while offset < 85051:
        url = f'https://combot.org/api/chart/all?limit=50&offset={offset}'
        response = requests.get(url=url, headers=headers)
        data = response.json()
        for item in data:
                if 't' in item:
                    result.append({
                        'name': item.get('t'),  # qq
                        'url': 'https://t.me/' + item.get('u'),
                        'language': item.get('l'),
                    })
        offset += 50
    return result


list_chats = get_data_file(headers=headers)

df = pd.DataFrame(
    {
        'Название': [list_chats[x]['name'] for x in range(0, len(list_chats))],
        'Ссылка': [list_chats[x]['url'] for x in range(0, len(list_chats))],
        'Язык': [list_chats[x]['language'] for x in range(0, len(list_chats))] })

df.to_excel('name.xlsx')
