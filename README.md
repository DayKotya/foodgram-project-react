# Foodgram

## Описание
Foodgram представляет из себя сайт - продуктовый помощник, на котором можно публиковать рецепты, добавлять чужие рецепты в избранное, подписываться на авторов. Также реализована возможность скачивать с сайта список покупок, в котором находятся ингредиенты добавленных рецептов.

## Техническое описание
Backend-часть проекта реализована на DRF, а Frontend - на React. Проект настроен для работы на удаленном сервере.

## Инструкция по установке
<p>1) Клонируйте репозиторий:</p>

```
git clone git@github.com:DayKotya/foodgram-project-react.git
```
<p>2) Для корректной работы проекта нужно настроить secrets для GitHub Actions. Для этого зайдите в settings вашего репозитория в раздел security, затем перейдите в подраздел Secrets and variables и там выберите Actions.</p>

Пример:
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
<p>Переменные DB_ENGINE, DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT используются для настройки базы данных.</p>
<p>Переменные DOCKER_USERNAME, DOCKER_PASSWORD нужны для входа в Dockerhub.</p>
<p>Переменные USER, HOST, PASSPHRASE нужны для доступа на удаленный сервер.</p>
<p>Переменная SECRET_KEY нужна для корректной работы Django.</p>
<p>Переменные TELEGRAM_TOKEN, TELEGRAM_TO нужны для отправки сообщения об успешном выполнении Workflow в Telegram.</p>

<p>3) Установите на удаленный сервер docker и docker-compose.</p>

<p>4) Затем перенесите на удаленный сервер файлы из директории infra/.</p>

<p>5) После этого выполните следующие команды:</p>

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
