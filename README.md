![foodgram workflow](https://github.com/Vokin-sm/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)

# Foodgram - Продуктовый помощник
Foodgram - это web-приложение для публикации своих рецептов. Авторизованный пользователь может выкладывать свои рецепты с описанием и приложенной картинкой, так же он может подписываться на других пользователей и следить за их рецептами, добавлять их в избранное и список покупок. Для удобства пользователей реализована фильтрация по тегам. Неавторизованный пользователь может посмотреть список рецептов, а так же авторизоваться для дальнейшего взаимодействия с приложением.

## Стек технологий
Python 3.8.5, Django 3, 2, 3, Django REST Framework, PostgreSQL, Docker-compose.

## Инструкция по развёртыванию 
Склонируйте репозиторий:
```bash
git clone https://github.com/Vokin-sm/foodgram-project-react.git
```
Выполните вход на удалённый сервер:
```bash
ssh <username>@<host>
```
Установите Docker и Docker-Compose, как это сделать, можно посмотреть в официальных источниках:
```bash
https://docs.docker.com/engine/install/ubuntu/
https://docs.docker.com/compose/install/
```
В директории infra в файле nginx.conf измените IP-адрес сервера и скопируйте этот файл вместе с файлом docker-compose.yml
на ваш удалённый сервер:
```bash
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
```
На удалённом сервере запустите Docker-compose:
```bash
docker-compose up -d
```
Убедитесь, что контейнеры запущены:
```bash
sudo docker ps -a
```
Создайте таблицы в базе данных:
```bash
sudo docker-compose exec backend python manage.py makemigrations --noinput
```
Сделайте миграции:
```bash
sudo docker-compose exec backend python manage.py migrate --noinput
```
Выполните команду для сбора статики:
```bash
sudo docker-compose exec backend python manage.py collectstatic --noinput
```

## Заполнение базы данных
По желанию можете наполнить базу некоторыми данными: 
```sudo docker-compose exec backend python manage.py loaddata fixtures/ingredients.json```

## Создание суперпользователя
Создайте супер пользователя:
```bash
sudo docker-compose exec backend python manage.py createsuperuser
```

## Приложение в работе
Для того чтобы посмотреть на работу приложения на моём рабочем сервере,
перейдите, пожалуйста, по адресу:
```http://130.193.40.172```
Тестовый суперпользователь: 
логин ```admin@test.ru```,
пароль ```admin```.
