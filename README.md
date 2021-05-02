# foodgram
![foodgram](https://github.com/OneMoreZanuda/foodgram-project/actions/workflows/main.yml/badge.svg)

# Описание
Проект **foodgram** - это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

# Разворачивание приложения на локальном сервере 
 
Для запуска веб-приложения на локальном сервере необходимо: 
1) Установить Docker;
2) Склонировать репозиторий; 
3) Открыть терминал и перейти в директорию проекта. Например: 
``` 
cd Dev\foodgram-project
```
4) Установить переменные окружения. Для этого в файле ".env.template" указать значение перечисленных переменных и сохранить его как ".env";
4) Запустить контейнер с PostgreSQL:
```
sudo docker-compose up -d db
```
5) Запустить контейнер с основным приложением:
```
sudo docker-compose up -d web
```
5) Собрать статические файлы в директории static:
```
sudo docker exec web python manage.py collectstatic
```
6) Выполнить миграции:
```
sudo docker exec web python manage.py makemigrations
sudo docker exec web python manage.py migrate
```
7) Создать суперпользователя:
```
sudo docker exec web python manage.py createsuperuser
```
8) (Опционально) Загрузить в базу данные о продуктах:
```
sudo docker exec web python manage.py loaddata /fixtures/fixtures.json
```

# Пример
Пример развернутого приложения **foodgram** доступен по адресу http://84.252.141.152/