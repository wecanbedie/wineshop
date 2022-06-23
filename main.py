import collections
import datetime

from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pandas import read_excel


foundation_date = datetime.datetime(year=1920, month=3, day=6)
foundation_year = foundation_date.year
last_day = datetime.datetime.today()
last_year = last_day.year
years_of_existing = last_year - foundation_year


env = Environment(
            loader=FileSystemLoader('.'),
            autoescape=select_autoescape(['html', 'xml'])
)   
wine_data = read_excel('wine.xlsx', sheet_name='Лист1', na_values=['N/A', 'NA'], keep_default_na=False)

winesorts = wine_data.to_dict(orient='records')


menu = collections.defaultdict(list)
for wine in winesorts:
    menu[wine['Категория']].append(wine)
      
template = env.get_template('template.html')


rendered_page = template.render(
    wine_age=str(years_of_existing),
    winecards=menu
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)


server = HTTPServer(
                ('0.0.0.0', 8000),
                SimpleHTTPRequestHandler
            )
server.serve_forever()

