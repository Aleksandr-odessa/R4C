import json
from os import write

import pandas as pd
import requests


bots = [{"model":"R2","version":"D2","created":"2024-12-12 23:59:59"},
        # {"model":"13","version":"XS","created":"2024-12-16 00:00:00"},
        # {"model":"X5","version":"LT","created":"2024-12-14 00:00:01"},
        # {"model":"R2","version":"A1","created":"2024-12-13 23:59:59"},
        # {"model":"R2","version":"B2","created":"2024-12-10 22:59:59"},
        # {"model":"R2","version":"B2","created":"2024-12-13 22:59:59"},
        # {"model":"R2","version":"B1","created":"2024-12-15 22:59:59"}
        ]

url = "http://127.0.0.1:8000/api/robots/create/"
url_week= "http://127.0.0.1:8000/api/robots/week/"
url_show = "http://127.0.0.1:8000/api/robots/show/"
url_order = "http://127.0.0.1:8000/order/"

def add_to_db(url_create, robots):
    for b in robots:
        try:
            req = requests.post(url_create, json=b)
            print(req.json())
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса: {e}")
        except json.JSONDecodeError:
            print("Ошибка при декодировании ответа сервера в JSON.")

def week_robots(url_week):
    response = requests.get(url_week)
    if response.status_code == 200:
        with open('output_file.xlsx', 'wb') as f:
            f.write(response.content)
        print("Файл успешно загружен и сохранен как output_file.xlsx")
    else:
        print(f"Ошибка при загрузке файла: {response.status_code}")

def order_robots(url):
    response = requests.post(url, json={"serial": "R2-D2", 'email':'p_alecs@mail.ru'})
    print(response.status_code)


def frame_with_count(data_in):
    df = pd.DataFrame(data_in)
    grouped = df.groupby(["model", "version"]).size().reset_index(name='count')
    g = grouped.rename(columns={
        'model': 'Модель',
        'version': 'Версия',
        'count': 'Количество за неделю'
    })

def write_to_excel(grouped_model):
    with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
        for model in grouped_model['Модель']:
            model_data = grouped_model[grouped_model['Модель'] == model]
            model_data.to_excel(writer, sheet_name=model, index=False)


data = [{'model': 'R2', 'version': 'D2'}, {'model': '13', 'version': 'XS'}, {'model': 'X5', 'version': 'LT'}, {'model': 'R2', 'version': 'A1'}, {'model': 'R2', 'version': 'B2'}, {'model': 'R2', 'version': 'B2'}, {'model': 'R2', 'version': 'D2'}, {'model': '13', 'version': 'XS'}, {'model': 'X5', 'version': 'LT'}, {'model': 'R2', 'version': 'A1'}, {'model': 'R2', 'version': 'B2'}, {'model': 'R2', 'version': 'B2'}, {'model': 'R2', 'version': 'B1'}, {'model': 'R2', 'version': 'D2'}, {'model': '13', 'version': 'XS'}, {'model': 'X5', 'version': 'LT'}, {'model': 'R2', 'version': 'A1'}, {'model': 'R2', 'version': 'B2'}, {'model': 'R2', 'version': 'B2'}, {'model': 'R2', 'version': 'B1'}, {'model': 'R2', 'version': 'D2'}, {'model': 'R2', 'version': 'D2'}, {'model': '13', 'version': 'XS'}, {'model': 'X5', 'version': 'LT'}, {'model': 'R2', 'version': 'A1'}, {'model': 'R2', 'version': 'B2'}, {'model': 'R2', 'version': 'B2'}, {'model': 'R2', 'version': 'B1'}]

add_to_db(url, bots)
# week_robots(url_show)
# data_frame(data)
# show_robot()

# order_robots(url_order)