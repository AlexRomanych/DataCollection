from clickhouse_driver import Client
import json

# Подключение к серверу ClickHouse
client = Client('localhost')

# Создание базы данных (если она не существует)
client.execute('CREATE DATABASE IF NOT EXISTS books_db')

# Создание таблицы
# Создание основной таблицы 'crashes'
client.execute('''
CREATE TABLE IF NOT EXISTS books_db.books (
    id UUID DEFAULT generateUUID(),
    title String,
    price_tax_excl String,
    price_tax_incl String,
    description String,
    availability Int64,
) ENGINE = MergeTree()
ORDER BY id
''')

print("Таблица создана успешно.")

# Чтение файла JSON
with open('books.json', 'r') as file:
    books = json.load(file)

# with open('crash-data.json', 'r') as file:
#     data = json.load(file)
#
# data = data['features']

# Вставка данных в таблицу
for book in books:
    # Вставка данных
    client.execute("""
    INSERT INTO books_db.books (
        title,
        price_tax_excl,
        price_tax_incl,
        description,
        availability
        ) VALUES""",
                   [(
                       book['title'],
                       book['price_tax_excl'],
                       book['price_tax_incl'],
                       book['description'],
                       book['availability']
                   )])

print("Данные введены успешно.")

# Проверка успешности вставки
result = client.execute("SELECT * FROM town_cary.crashes")
print("Первая вставленная запись:", result[0])
