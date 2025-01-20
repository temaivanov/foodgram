
# Проект Foodgram

Проект "Foodgram" – это онлайн-каталог пользовательских рецептов,и утилита для составления списка покупок. Также, это заключительный проект курса по бэкенд-разработке на Python. 

С помощью этого сервиса пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Адрес: https://diplomaproject.zapto.org/ (в настоящее время хост более недоступен, требуется передеплой на другой хост.)

## Установка и локальный запуск
Выполните следующие шаги для того чтобы запустить веб-приложение локально на вашем компьютере. Для запуска потребуется установить Docker.

1. Клонируйте репозиторий на ваш компьютер и перейдите в него в командной строке:

```
git@github.com:temaivanov/foodgram.git

cd foodgram
```

2. В директории foodgram cоздайте файл .env, и заполните его своими данными (credentials) по примеру ниже. 
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

3. Cоздайте и активируйте виртуальное окружение Python из директории foodgram:
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



## Скриншоты

![Заглавная страница; без логина](https://github.com/temaivanov/foodgram_images/blob/main/Screenshot%202025-01-19%20at%2021.19.20.png)

![Заглавная страница; c логином](https://github.com/temaivanov/foodgram_images/blob/main/screencapture-diplomaproject-zapto-org-recipes-2024-10-16-11_27_28.png)

![Страница рецепта; c логином](https://github.com/temaivanov/foodgram_images/blob/main/screencapture-diplomaproject-zapto-org-recipes-5-2024-10-16-11_29_33.png)

![Страница списка покупок; c логином](https://github.com/temaivanov/foodgram_images/blob/main/screencapture-diplomaproject-zapto-org-cart-2024-10-16-11_29_01.png)

![Страница подписок; c логином](https://github.com/temaivanov/foodgram_images/blob/main/screencapture-diplomaproject-zapto-org-subscriptions-2024-10-16-11_28_28.png)

![Страница смены пароля; c логином](https://github.com/temaivanov/foodgram_images/blob/main/screencapture-diplomaproject-zapto-org-change-password-2024-10-16-11_28_40.png)


## Автор

Выполнил Артем Иванов https://github.com/temaivanov

artyom.ivanov.spb@gmail.com

