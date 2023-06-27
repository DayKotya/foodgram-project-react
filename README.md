# Foodgram
IP - 158.160.59.223

Логин администратора - admin
Пароль администратора - admin

## Описание
Foodgram представляет из себя сайт - продуктовый помощник, на котором можно публиковать рецепты, добавлять чужие рецепты в избранное, подписываться на авторов. Также реализована возможность скачивать с сайта список покупок, в котором находятся ингредиенты добавленных рецептов.

## Техническое описание
Backend-часть проекта реализована на DRF, а Frontend - на React. Проект настроен для работы на удаленном сервере.

## Инструкция по установке
Клонируйте репозиторий:
```
git clone git@github.com:DayKotya/foodgram-project-react.git
```
Для корректной работы проекта нужно создать actions secrets. Пример:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django-insecure-7bxeu1gdyx#1(fb68=tql@7f
DOCKER_USERNAME=username
DOCKER_PASSWORD=password
HOST=160.25.31.137
TELEGRAM_TOKEN=a3#fdssp45igmR31a
TELEGRAM_TO=1535489538406
USER=username
PASSPHRASE=password
```
Переменные DB_ENGINE, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT используются для настройки базы данных.
Переменные DOCKER_USERNAME, DOCKER_PASSWORD нужны для входа в Dockerhub.
Переменные USER, HOST, PASSPHRASE нужны для доступа на удаленный сервер.
Переменная SECRET_KEY нужна для корректной работы Django.
Переменные TELEGRAM_TOKEN, TELEGRAM_TO нужны для отправки сообщения об успешном выполнении Workflow в Telegram.
***
Установите на удаленный сервер docker и docker-compose.
***
Затем перенесите на удаленный сервер файлы из директории infra/.
***
После этого запустите следующие команды:
```
sudo docker-compose up -d --build
sudo docker-compose exec backend python manage.py makemigrations
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --no-input
```
## Информация по использованию
Пользователь будет выбирать ингредиенты из предустановленного списка, который самостоятельно может создать администратор. Для предзагрузки базы данных с ингредиентами можно использовать следующую команду:
```
docker-compose exec backend python manage.py ingredients_script
```
Для успешного создания рецептов нужно добавить через админку несколько тэгов. Например: обед, завтрак, ужин.
