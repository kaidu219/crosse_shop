# Интернет-магазин одежды

## Описание проекта
Проект представляет собой веб-приложение интернет-магазина одежды, реализованное с использованием фреймворков Django и Django Rest Framework.

## Основной функционал
Проект предоставляет следующие возможности:

- Регистрация и аутентификация пользователей
- Просмотр список товаров
- Просмотр детальной информации о товаре
- Добавление товаров в избранное

## Установка
Для начала, клонируйте репозиторий проекта:

`git clone https://github.com/kaidu219/clothing_store.git`

Создайте и активируйте виртуальное окружение:

`python -m venv venv`
`source venv/bin/activate`

Установите зависимости:

`pip install -r requirements.txt`

Примените миграции:

C начало надо сделать миграцию для приложения product


`python manage.py makemigrations product`
`python manage.py migrate product`


Затем для users

`python manage.py makemigrations users`
`python manage.py migrate users`

Запустите проект:

`python manage.py runserver`

## Использованные технологии
- Python
- Django
- Django REST Framework
- Django аутентификация и авторизация
- Django ORM
