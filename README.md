
# Проект Foodgram
Проект "Foodgram" – это "продуктовый помощник". На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект доступен по адресу https://diplomaproject.zapto.org/recipes
Для доступа в админ-панель, свяжитесь со мной: artyom.ivanov.spb@gmail.com (можно через "Пачку")


## Установка и локальный запуск

1. Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:temaivanov/foodgram.git

cd foodgram
```

2. Создайте файл .env и заполните его своими данными по примеру ниже. 
```
# --- Django-доступы ---
DJANGO_SECRET_KEY='key'
DJANGO_ALLOWED_HOSTS=123.123.123.123,website.com,127.0.0.1,localhost
DJANGO_DEBUG=False

# --- Postgres-доступы ---
# Имя пользователя PostgreSQL
POSTGRES_USER={username}
# Пароль пользователя PostgreSql
POSTGRES_PASSWORD={password}
# Какая база будет создана при инициализации Postgres
POSTGRES_DB={database}
# К какой базе необходмо подключиться
DB_NAME={database}
# Где хостится БД. В Докере это имя сервиса db.
DB_HOST={service_name}
# Порт, на котором принимает запросы БД.
DB_PORT={port}

# --- Настройки для CSRF ---
CSRF_TRUSTED_ORIGINS=https://вашдомен.com
```

3. Cоздайте и активируйте виртуальное окружение
```
python3 -m venv venv

source venv/bin/activate
```

4. Установите зависимости
```
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```

5. Перейдите в папку /foodgram/infra и выполните команду 
 ```
docker-compose up
```

6. Примените миграции в запущенном контейнере, создайте суперюзера, импортируйте ингридиенты.
Статика фронтенда и бекенда соберется при запуске образа, но миграции нужно сделать самостоятельно.
Если запускать CI/CD, то миграции применятся автоматически.
```
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py loaddata ingredients_transformed.json
```

Теперь проект запущен на локальном компьютере в нетворке докер-контейнеров и доступен по адресу http://localhost/


## Технологии бекенда

- Django 4.2.16
- Django Rest Framework 3.15.2
- gunicorn 20.1.0
- Docker
- Nginx

## Автор

Выполнил Артем Иванов https://github.com/temaivanov
