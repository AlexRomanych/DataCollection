import requests
import json
from geopy.geocoders import Nominatim


def get_venues(category, location, limit=40):
    """Функция для получения мест по категории и локации с помощью Foursquare API"""

    API_KEY = "fsq3vqL8ASNSOiJukIN7+foodRI7QXRU4oDZwZ/RsKvHzpg="

    # Используем geopy для получения географических координат по названию локации
    geolocator = Nominatim(user_agent="my_geocoder")
    locate = geolocator.geocode(location)
    latitude = locate.latitude
    longitude = locate.longitude

    print('>' * 10)
    print(f'Детальное местоположение: {locate.address}')
    print(f'Координаты: широта: {latitude}, долгота: {longitude}')
    print('_' * 150)

    # Формируем URL для запроса к API
    url = f'https://api.foursquare.com/v3/places/search'
    headers = {
        "Accept": "application/json",
        "Authorization": API_KEY
    }

    # Задаем строку поиска + геоданные + нужные поля для уменьшения трафика
    if limit > 40:
        limit = 40

    params = {
        'query': category,
        'll': f'{latitude},{longitude}',
        'fields': 'categories,location,rating',
        'limit': limit
    }

    # Отправляем запрос и получаем ответ
    response = requests.get(url, params=params, headers=headers)
    search_data = json.loads(response.text)

    # Извлекаем данные о местах из ответа
    data = search_data['results']

    # Выводим результаты
    for place in data:
        print(f'Название: {place['categories'][0].get('name')} ||| Сокращенное: {place['categories'][0].get('short_name')}')
        print(f'Адрес: {place.get('location').get('formatted_address')}')

        rating = 'Рейтинг отсутствует!' if 'rating' not in place else place.get('rating')

        print(f'Рейтинг: {rating}')
        print('-' * 100)


if __name__ == '__main__':
    category = input("Введите интересующую вас категорию (например, кофейни, музеи): ")
    location = input("Введите город или местоположение: ")
    limit = input("Введите количество объектов (10 по умолчанию): ")
    limit = int(limit) if limit else 10
    print(limit)

    get_venues(category, location, limit)
