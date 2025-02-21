import sqlite3
import pandas as pd

# Подключение к базе
conn = sqlite3.connect('db.sqlite3')

# Загрузка CSV
df = pd.read_csv('D:/Dev/api_yamdb/api_yamdb/static/data/comments.csv')

# Запись данных в таблицу
df.to_sql('table_name', conn, if_exists='replace', index=False)

# Закрытие соединения
conn.close()