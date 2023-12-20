# Продуктовый помощник Foodgram
[![Foodgram workflow](https://github.com/Nastasya-M/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/Nastasya-M/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

### Продуктовый помощник Foodgram - это сервис, с помощью которого пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. 
```
Для работы проекта был разработан и настроен CI/CD.
```

### Технологи проекта:
```
Django 3.2
Django REST framework
Python 3.7.9
Docker
Nginx
GitHub Actions
Postgres
```

### Как запустить проект:
Клонировать репозиторий:
```
git clone https://github.com/Nastasya-M/foodgram-project-react
```

Для работы workflow необходимо добавить переменные окружения в Secrets GitHub:
```
DOCKER_USERNAME=<имя пользователя DockerHub>
DOCKER_PASSWORD=<пароль DockerHub>

USER=<username для подключения к удаленному серверу>
HOST=<ip-адрес сервера>
PASSPHRASE=<пароль для сервера (если установлен)>
SSH_KEY=<SSH-ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<id вашего Телеграм-аккаунта>
TELEGRAM_TOKEN=<Телеграм-токен вашего бота>
```
Пример заполнения .env файла:
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
```
Вход на удаленный сервер:
```
ssh <username>@<host>
```

Установка Docker:
```
sudo apt install docker.io
```

Установка Docker-compose:
```
sudo curl -L "https://github.com/docker/compose/releases/download/v2.17.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Скопируйте файлы docker-compose.yaml и nginx.conf из директории /infra/ локального проекта на сервер

```
scp docker-compose.yaml <username>@<host>:/home/<username>/
scp -r nginx/ <username>@<host>:/home/<username>/
```
После успешного деплоя зайдите на боевой сервер и выполните команды:
```
sudo docker-compose up -d
sudo docker-compose exec web python manage.py migrate # примените миграции
sudo docker-compose exec web python manage.py collectstatic --no-input # подгрузите статику
sudo docker-compose exec web python manage.py createsuperuser # создайте суперпользователя
sudo docker-compose exec web python manage.py import_ingredients # загрузите ингридиенты
```
### Автор
[Настасья Мартынова](https://github.com/Nastasya-M)
