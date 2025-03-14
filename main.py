import collections
import datetime
import argparse

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel



def main():
    parser = argparse.ArgumentParser(description='Ваш путь к файлу.')
    parser.add_argument('filepath', type=str, help='Укажите ваш путь к excel-файлу.')
    arg = parser.parse_args()

    wineshop_foundation = 1920
    current_date = datetime.datetime.today()
    current_year = current_date.year
    winery_age = current_year - wineshop_foundation


    env = Environment(
                loader=FileSystemLoader('.'),
                autoescape=select_autoescape(['html', 'xml'])
    )   
    excel_file = read_excel(arg.filepath, sheet_name='Лист1', na_values=['N/A', 'NA'], keep_default_na=False)

    database_drinks = excel_file.to_dict(orient='records')
    #Надеюсь такое название подойдёт

    menu = collections.defaultdict(list)
    for wine in database_drinks:
        menu[wine['Категория']].append(wine)
        
    template = env.get_template('template.html')


    rendered_page = template.render(
        winery_age=winery_age,
        winecards=menu
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


    server = HTTPServer(
                    ('0.0.0.0', 8000),
                    SimpleHTTPRequestHandler
                )
    server.serve_forever()


if __name__ == '__main__':
    main()

