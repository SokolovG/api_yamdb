**[English](#english) | [Русский](#russian)**

## English

### About Api YAmdb
Api YAmdb is a RESTful API service that provides access to the YaMdb database. This service allows users to work with titles, categories, genres, and reviews.

### Key Features
- User authentication and authorization
- #
- #
- #

### Available Endpoints
- #
- #
- #

### Tech Stack
- Backend: Django + DRF
- Database: Sqlite + Redis
- Authentication: JWT tokens
- Documentation: ReDoc

### Installation and Setup
1. Clone the repository:
```bash
git clone https://github.com/SokolovG/api_yamdb.git
cd api_yamdb
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # For Linux/MacOS
# or
venv\Scripts\activate  # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install and configure Redis:
```bash
# For MacOS (using Homebrew)
brew install redis
brew services start redis

# For Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server

# For Windows
# Download and install Redis from https://github.com/microsoftarchive/redis/releases

# Test Redis connection
redis-cli ping  # Should return PONG
```

4. Create .env file in the root directory and set up environment variables:
```bash
touch .env  # For Linux/MacOS
# Add these variables to .env:
SECRET_KEY=your_secret_key
```

5. Apply migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

7. The application will be available at:
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/redoc/

## Russian

### О проекте Api YAmdb
Api YAmdb - это RESTful API сервис, предоставляющий доступ к базе данных YaMdb. Этот сервис позволяет пользователям работать с произведениями, категориями, жанрами и отзывами.

### Основные возможности
- Аутентификация и авторизация пользователей
- #
- #
- #

### Доступные эндпоинты
- #
- #
- #

### Технологический стек
- Бэкенд: Django + DRF
- База данных: Sqlite + Redis
- Аутентификация: JWT токены
- Документация: ReDoc

### Установка и запуск
1. Клонируйте репозиторий:
```bash
git clone https://github.com/SokolovG/api_yamdb.git
cd api_yamdb
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
# или
venv\Scripts\activate  # Для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Установите и настройте Redis:
```bash
# Для MacOS (используя Homebrew)
brew install redis
brew services start redis

# Для Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis-server

# Для Windows
# Скачайте и установите Redis с https://github.com/microsoftarchive/redis/releases

# Проверка подключения к Redis
redis-cli ping  # Должен вернуть PONG
```

4. Создайте файл .env в корневой директории и настройте переменные окружения:
```bash
touch .env  # Для Linux/MacOS
# Добавьте эти переменные в .env:
SECRET_KEY=your_secret_key
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Запустите сервер разработки:
```bash
python manage.py runserver
```

7. Приложение будет доступно по адресам:
- API бэкенда: http://localhost:8000
- Документация API: http://localhost:8000/redoc/


### Импорт CSV файлов

1. Установите зависимости (добавлена зависимость от pandas):
```bash
pip install -r requirements.txt
```

2. Расположение загружаемых файлов: static/data:

3. Запуск импорта:
```bash
python manage.py import_csv 
```

