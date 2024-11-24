import requests
from lxml import html
import csv
import time

# Задаем клиента
ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'
headers = {'User-Agent': ua}


def get_page_from_net():
    """Получаем данные с сайта"""
    url = 'https://news.mail.ru/'
    response = requests.get(url, headers=headers)
    return response.content


def get_page_from_file():
    """Получаем данные из файла, это в нужно в процессе разработки
    потому, что сервис получает геолокацию по ip и перекидывает на другой вид страницы"""
    with open('mail.news.ru.html', 'r', encoding='utf-8') as file:
        data = file.read()
        return data


def get_tree():
    """Получаем дерево"""
    content = get_page_from_net()
    # content = get_page_from_file()
    tree = html.fromstring(content)
    return tree


def get_links():
    """Получаем ссылки из главного блока новостей"""
    tree = get_tree()
    # Находим все ссылки на новости в главном блоке м атрибутом data-logger='news__MainTopNews'
    news_links = tree.xpath("//div[@data-logger='news__MainTopNews']//a/@href")
    return news_links


# Данные для записи в CSV файл
def save_csv(data):
    """Сохраняем данные в CSV файл"""

    # Открываем файл для записи в режиме 'w' (write)
    with open('news.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['news_title', 'news_text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')     # Создаем объект writer
        writer.writeheader()                                                        # Записываем заголовок
        writer.writerows(data)                                                      # Записываем остальные данные


def main():
    """Основной блок"""

    links = get_links()

    news = []
    for link in links:

        print(f'Парсим новость: {link}')
        time.sleep(3)

        response = requests.get(link, headers=headers)
        page_tree = html.fromstring(response.content)

        try:
            # Каждая новость на странице имеет атрибут data-article-index='0'
            # Получаем название новости
            article_title = page_tree.xpath("//div[@data-article-index='0']//h1/text()")[0].strip().replace('\xa0', ' ')

            # Содержимое новости находится в тегах p
            # получаем содержимое в виде массива
            article_text_list = page_tree.xpath("//div[@data-article-index='0']//p")

            # Собираем в одну строку
            article_text = ''
            for article_text_item in article_text_list:
                article_text += article_text_item.text.strip().replace('\xa0', ' ')

            news.append(
                {
                    'news_title': article_title,
                    'news_text': article_text
                })

            print('Парсинг: успешно')

        except:
            print('Парсинг: или странице не новостная, или другая ошибка')

    save_csv(news)  # Сохраняем данные в CSV файл


if __name__ == "__main__":
    main()
