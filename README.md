# Тестовое задание

Данный репозиторий представляет собой решение тестового задания изложенного
по данной [ссылке](https://www.craft.do/s/n6OVYFVUpq0o6L)

## Описание проекта

Реализован сервис для планирования и рассылки сообщений. Основной стек
технологий в проекте: Django, Django REST Framework, celery, PostgreSQL
(необходима предварительная установка)

## Разворачивание проекта для разработчика

1. В папке post_service/post_service необходимо создать .env файл. В корне
проекта имеется пример данного файла.
2. В postgresql создать базу данных в соотвествии с указанной в .env файле
(в примере post_service)
3. Необходимо развернуть redis, можно выполнить команду (требуется установленный
докер):

```console
docker run -d -p 6379:6379 redis
```
4. Развернуть виртуальное окружение, проект реализован на python 3.11.2
установить пакеты

```console
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
5. Выполнить миграции, создать пользователя, запустить сервер
```console
python post_service/manage.py migrate
python post_service/manage.py createsuperuser
python post_service/manage.py runserver
```
6. Запустить celery

```console
python post_service/manage.py migrate
python post_service/manage.py createsuperuser
python post_service/manage.py runserver
```

## Алтернативный запуск через docker
В корне проекта имеется docker-compose.yaml файл и файл окружения используемы. 
Для разворачивания проекта на локальном хосте можно при наличии docker 
выполнить команду:
```console
docker-compose up
```
## Методы АПИ
Для использования методов API требуется создать пользователя. При разворачивании
проекта через manage.py можно создать пользователся коммандой как указано выше.
В случае разворачивания проекта через докер можно зарегистрировать пользователя
через интерфейс реалихованный в проекте перейдя по адресу 127.0.0.1.

В проекте использована простая авторизация по токену. Предварительно требуется
получить токен по запросу /auth/ и включить его в заголовки передаваемых 
запросов.

После запуска проекта, доступен swagger со описанием методов по адресу /docs.
При запуске проекта в docker по адресу 127.0.0.1/docs.

## Особенности
Все сущности, запросы реализованы согласно ТЗ, за исключением особенности
сущности сообщение (Message). В ТЗ не указано прямо какие статусы может 
принимать сообщение. Произвольно приняты следующие варианты статусв:

```
status_choises = (
    ('processing', 'Отправка сообщения'),
    ('sent', 'Отправлено'),
    ('error', 'Ошибка'),
    ('expired', 'Доставка просрочена')
)
```
**processing** - сообщения создаются в тот момент когда celery начинает обработку
рассылки и отправку запросов на API и получают данный статус.  
**sent** - сообщения получают после получения ответа от API об успешной 
обработке запроса.  
**error** - сообщения получают после получения ответа от API с ошибкой выполнения
или при наличии возможности соединения с API в момент отправки сообщения.
**expired** - сообщения получают в том случае, если при старте рассылки они 
не были отправлены вовремя.