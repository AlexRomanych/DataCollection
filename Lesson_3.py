from pymongo import MongoClient
import json
import hashlib

# создание экземпляра клиента
connection = MongoClient('localhost', 27017)
# connection = MongoClient('127.127.126.51', 27017)  # У меня Open Server повесил на этот ip

# подключение к базе данных и коллекции
books_db = connection['books_db']  # Создаем БД books_db
books_collection = books_db['books_collection_name']  # Создаем коллекцию books_collection

# connection.drop_database('books_collection')
# books.delete_many({})

# Чтение файла JSON
with open('books.json', 'r') as file:
    all_books = json.load(file)

# Запихиваем в коллекцию книжки
# books_collection.insert_many(all_books)
# или
for book in all_books:
    # Создадим чего-нибудь уникальное, например хэш и в _id запишем его
    hash_string_binary = (book.get('title') + book.get('description')).encode()
    book_hash = hashlib.sha256(hash_string_binary).hexdigest()
    book['_id'] = book_hash
    books_collection.insert_one(book)

# Настраиваем шаблон отображение данных
projection = {
    "_id": 0,
    "title": 1,
    "availability": 1,
    "price_tax_excl": 1,
    "price_tax_incl": 1,
    "description": 1,
}

# Тут разные запросы:

# Например, количество в наличии от 20 до 25
query = {'availability': {'$gte': 20, '$lte': 25}}

# Например, в названии есть повторение Sea
query = {'title': {'$regex': 'Sea'}}

# Например, в названии есть слово sea и в описании есть слово man
query = {'$and': [
    {'title': {'$regex': 'Sea'}},
    {'description': {'$regex': 'man'}}
]}

# Например, в названии есть слово sea и в описании есть слово man без учета регистра
query = {
    'title': {
        '$regex': 'sea',
        '$options': 'i'
    },
    'description': {
        '$regex': 'man',
        '$options': 'i'
    }
}

# И так можно до бесконечности

# Выполняем запрос
books = books_collection.find(query, projection)

# Выводим в консоль
count = 0
for book in books:
    print(book)
    count += 1

print(f'Количество найденных документов: {count}')
