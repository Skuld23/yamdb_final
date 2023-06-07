[![Yamdb workflow](https://github.com/Skuld23/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/Skuld23/yamdb_final/actions/workflows/yamdb_workflow.yml)
# Проект Яндекс-Практикума YaMDb

## Описание 
Данный проект реализует REST API для сервиса YaMDb — базы отзывов о книгах, музыке и фильмах.<br>
Сервис YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен через интерфейс администратора.<br>
Пользователи могут оставить к произведениям текстовые отзывы и поставить произведению оценку от 1 до 10. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг.

В данном проекте посредством API реализованы следующие возможности:

- **auth**: аутентификация<br>
  (отправка confirmation_code на указанный email, получение JWT-токена в обмен на email и confirmation_code)
- **users**: пользователи<br>
  (получение списка всех пользователей, создание пользователя, получение данных пользователя, изменение данных пользователя, удаление пользователя, получение данных своей учетной записи, изменение данных своей учетной записи)
- **titles**: произведения<br>
  (получение списка всех произведений, добавление произведения, получение информации о произведении, обновление информации о произведении, удаление произведения)
- **categories**: категории произведений<br>
  (получение списка всех категорий, создание категории, удаление категории)
- **genres**: жанры произведений, одно произведение может быть привязано к нескольким жанрам<br>
  (получение списка всех жанров, создание жанра, удаление жанра)
- **reviews**: отзывы на произведения<br>
  (получение списка всех отзывов, создание отзыва, получение отзыва, обновление отзыва, удаление отзыва)
- **comments**: комментарии к отзывам<br>
  (получение списка всех комментариев к отзыву, создание комментария для отзыва, получение комментария для отзыва, обновление комментария к отзыву, удаление комментария к отзыву)

Перечень запросов к ресурсу можно посмотреть в описании API после настройки и запуска проекта

```
http://127.0.0.1:8000/redoc/
```

## Стек технологий
- проект написан на Python с использованием веб-фреймворка Django REST Framework
- библиотека Simpsle JWT - работа с JWT-токеном
- библиотека django-filter - фильтрация запросов
- база данных - SQLite
- система управления версиями - git
- gunicorn

## Алгоритм регистрации новых пользователей

1. Пользователь отправляет POST-запрос с email и username на /api/v1/auth/signup/.
2. Сервис YaMDB отправляет письмо с confirmation_code на email адрес пользователя.
3. Пользователь отправляет POST-запрос с username и confirmation_code на /api/v1/auth/token/. В ответ ему придет JWT-токен.
4. После получения JWT-токена пользователь может работать с API проекта, отправляя этот токен при каждом запросе.

## Установка
Клонировать репозиторий:

```
git clone git@github.com:Skuld23/infra_sp2.git
cd infra_sp2
```

* Переходим в папку с файлом docker-compose.yaml:

```
cd infra
```

* Разворачиваем образы и сразу запускаем проект:

```
docker-compose up -d --build
```

* Выполняем миграции:

```
docker-compose exec web python manage.py migrate
```

* Создаем суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```

* Подключаем статику:

```
docker-compose exec web python manage.py collectstatic --no-input
```

* Заполняем базу исходными данными:

```
docker-compose exec web python manage.py loaddata fixtures.json
```

* Создаем дамп (резервную копию) базы:

```
docker-compose exec web python manage.py dumpdata > fixtures.json
```

* Загрузить в базу данные из дампа. Файл fixtures.json разместить в папке с Dockerfile (или в корневой папке проекта, и тогда указать путь ../fixtures.json):

```
docker-compose exec web python manage.py loaddata fixtures.json
```

* Проверяем работоспособность приложения:

```
 http://localhost/admin/
```

### Файл .env:
#### Шаблон наполнения файла (в /infra):
```
DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы даннцых
POSTGRES_USER=username # логин для подключения к базе данных
POSTGRES_PASSWORD=password # пароль для подключения к БД 
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
``

## После успешного деплоя
* Создать суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```

* Для проверки работоспособности приложения:
```
http:/158.160.33.198/admin/
```

## Документация для YaMDb доступна по адресу:
```
http:/158.160.33.198/redoc/
```
