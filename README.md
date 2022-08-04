![example workflow](https://github.com/AndreyVnk/foodgram-project-react/actions/workflows/main.yaml/badge.svg)
# Foodgram project

**Foodgram project** - проект, поддерживающий обмен данными в формате *JSON*. Развернут в 4х Docker контейнерах (db, backend, frontend, nginx).

Настроены CI и CD: автоматический запуск тестов (PEP8), обновление образов на Docker Hub,автоматический деплой на боевой сервер при push в ветку master.

Cистема аутентификация реализована через получение токена. Функционал API предоставляет следующие ресурсы: 

- recipes/ (рецепты) 
- ingredients/ (ингредиенты)
- tags/ (тэги)
- users/ (пользователи)

**Технологии:**

* Python 3
* Django Rest Framework
* Djoiser
* PostgreSQL
* Docker

## Запуск проекта ##
### 1. Склонировать репозиторий
```
git clone https://github.com/AndreyVnk/foodgram-project-react.git && cd foodgram-project-react/
```
### 2. Добавить Action Secrets
```
DOCKER_USERNAME=<docker login>
DOCKER_PASSWORD=<docker password>
USER=<server user>
HOST=<server ip address>
PASSPHRASE=<password phrase to ssh key>
SSH_KEY=<public key> # cat ~/.ssh/id_rsa (linux) на машине имеющей доступ к серверу
TELEGRAM_TO=<chat ID> # для отправки уведомлений в телеграм через бота
TELEGRAM_TOKEN=<bot token> # для отправки уведомлений в телеграм через бота
SECRET_KEY=secret django key
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
### 3. Изменить настройки nginx.conf в папке infra/
```
server_name <server_ip_address>;
```
### 4. Подготовьте сервер
Установите docker и docker-compose
```
https://docs.docker.com/engine/
```
### 5. Выполнить копирование файлов docker-compose.yaml и nginx.conf на сервер
```
scp infra/docker-compose.yaml <user>@<ip_address>:/home/<user>/docker-compose.yaml
scp infra/nginx.conf <user>@<ip_address>:/home/<user>/nginx.conf
```
### 6. Выполнить commit и push проекта
```
git add .
git commit -m 'something'
git push
```
### 7. На сервере выполнить следующие команды
```
sudo docker-compose exec foodgram_backend python manage.py migrate
sudo docker-compose exec foodgram_backend python manage.py collectstatic --no-input
sudo docker-compose exec foodgram_backend python manage.py createsuperuser
sudo docker-compose exec foodgram_backend python manage.py load_ingredients
```
Эндпоинты, описанные в документации доступны на корневом адресе проекта: http://<server_ip_address>/api/. Документация к API доступна на http://<server_ip_address>/api/docs/ .

Пример проекта доступен по http://84.201.130.224/ . Документация к API - http://84.201.130.224/api/docs/ . 

**Автор** 

AndreyVnk
