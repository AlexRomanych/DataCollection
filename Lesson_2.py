import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint

# Выполнить скрейпинг данных в веб-сайте http://books.toscrape.com/
# и извлечь информацию о всех книгах на сайте во всех категориях:
# - название
# - цену
# - количество товара в наличии (In stock (19 available)) в формате integer
# - описание
# Затем сохранить эту информацию в JSON-файле.

# Будем стучаться от Safari
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
url = "https://books.toscrape.com/catalogue/"
headers = {'User-Agent': ua}

# Создаем сессию для меньшей подозрительности
session = requests.Session()

# Задаем начальные параметры
books = []
page_id = 1

while True:

    # Стучимся на сервер books.toscrape.com
    page_url = url + f'page-{page_id}.html'

    response = session.get(page_url, headers=headers)

    # Создаем объект BeautifulSoup
    soap = BeautifulSoup(response.text, 'html.parser')

    books_divs = soap.find_all('article', class_='product_pod')
    # books_divs = soap.find_all('article', class_='product_pod', limit=1)

    for book_div in books_divs:

        book_anchor = book_div.find('a', href=True)

        if book_anchor:
            book_link = url + book_anchor.get('href')

            response = session.get(book_link, headers=headers)
            soap_book = BeautifulSoup(response.text, 'html.parser')

            book_title = soap_book.find('h1').getText()
            book_title = book_title if book_title else 'Noname'

            book_table = soap_book.find_all('tr')

            book_price_excl = 'No price'
            book_price_incl = 'No price'
            book_availability = 0
            book_description = 'No description'

            for row in book_table:

                # Две цены, в условии задачи не сказано, какая нужна
                # и не указан формат, поэтому выводим в текстовом
                if row.find('th').getText() == 'Price (excl. tax)':
                    book_price_excl = row.find('td').getText().replace('Â', '')

                if row.find('th').getText() == 'Price (incl. tax)':
                    book_price_incl = row.find('td').getText().replace('Â', '')

                if row.find('th').getText() == 'Availability':
                    try:
                        book_availability = int(
                            row.find('td').getText().replace('In stock (', '').replace(' available)', ''))
                    except Exception:
                        book_availability = 0

            book_description_p = soap_book.find('p', class_='')
            if book_description_p:
                book_description = book_description_p.getText()

            book = {
                'title': book_title,
                'price_tax_excl': book_price_excl,
                'price_tax_incl': book_price_incl,
                'description': book_description,
                'availability': book_availability,
            }

            books.append(book)

    print(f'Обработка страницы {page_id}')

    if not soap.find('li', class_='next'):
        break

    page_id += 1

# pprint(books)

# Записываем данные в файл в формате JSON
with open('books.json', 'w') as f:
    json.dump(books, f, indent=2)
