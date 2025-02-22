from django.core.management.base import BaseCommand
import sqlite3
import pandas as pd
import os
import logging

CSV_DIR = 'static/data'
CSV_TO_TABLE = [
    ('genre.csv', 'content_genre'),
    ('category.csv', 'content_category'),
    ('genre_title.csv', 'content_titlegenre'),
    ('titles.csv', 'content_title'),
    ('comments.csv', 'reviews_comment'),
    ('review.csv', 'reviews_review'),
    ('users.csv', 'users_user'),
]

FORMATTER = '%(asctime)s — %(levelname)s — %(message)s'

logging.basicConfig(level=logging.INFO, format=FORMATTER)


class Command(BaseCommand):
    """Команда импорта CSV файлов"""

    def handle(self, *args, **kwargs):
        conn = sqlite3.connect('db.sqlite3')
        for csv_file, table in CSV_TO_TABLE:
            df = pd.read_csv(os.path.join(CSV_DIR, csv_file), delimiter=',')
            try:
                df.to_sql(table, con=conn, if_exists='append', index=False)
                logging.info(f'Файл {csv_file} загружен в таблицу: {table}')
            except sqlite3.IntegrityError as err:
                logging.error(err)
        conn.commit()
        conn.close()
