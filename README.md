# Job Board

REST API для платформы вакансии с возможностью:

- Создании компании и публикации вакансии

- Отклика кандидата на вакансии

- Один пользователь может быть работодателем и кандидатом


Роли определяются динамически на основе:

- Есть компании -> Работодатель
- Есть отклики -> Кандидат
- Есть и то и другое -> Обе роли

## Стек

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL (или SQLite для разработки)
- Django-filter
- Swagger / OpenApi

## Запуск проекта

1. Клонирование

git clone https://github.com/jlxinn/job_board.git

cd job_board

2. Установка зависимостей

pip install -r requirements.txt

pip install -r requirements-dev.txt (для разработчиков)

3. Миграции

python manage.py migrate

4. Запуск сервера

python manage.py runserver


## API документации

Swagger доступен по адресу:

api/v1/docs/#/

## Основные сущности

### Company

- Принадлежит пользователю(owner)
- Используется для публикации вакансии

### Job

- Вакансия
- Связана с компанией
- Имеет статус активности 

### Application

- Отклик пользователя на вакансию
- Содержит статус (pending/accepted/rejected)


## Основные endpoints

### Companies

GET     `/api/v1/companies/`  
POST    `/api/v1/companies/`  
GET     `/api/v1/companies/{id}/`  
PUT     `/api/v1/companies/{id}/`  
DELETE  `/api/v1/companies/{id}/`  

GET     `/companies/my/`  


### Jobs

GET     `/api/v1/jobs/`  
POST    `/api/v1/jobs/`  
GET     `/api/v1/jobs/{id}/`  
PUT     `/api/v1/jobs/{id}/`  
DELETE  `/api/v1/jobs/{id}/`  

GET     `/jobs/my/`  


### Applications

GET     `/api/v1/applications/`  
POST    `/api/v1/applications/`  
GET     `/api/v1/applications/{id}/`  
PUT     `/api/v1/applications/{id}/`  
DELETE  `/api/v1/applications/{id}/`  

GET     `/api/v1/applications/my/`  
GET     `/api/v1/applications/incoming/`  


## Фильтрация и поиск

### Jobs и во всех других сущностях

- Поиск:

?search=python

?search=CompName

- Фильтры:

?location=abc

?min_salary=123

?max_salary=123

?title=abc

- Сортировка:

?ordering=salary

?ordering=created_at 


### Applications

- Фильтры

?status=pending


## Пагинация 

По дефолту:

?page=1
?page_size=10


## Permissions

- Только владелец компании может создавать вакансии
- Только владелец вакансии может управлять откликами
- Пользователь может откликаться только от своего имени
- Запрещено редактировать чужие данные


## Тестирование

- Запуск всех тестов:

python manage.py test

-  конкретного Apps:

python manage.py test apps.jobs


## Бизнес правила

- Нельзя откликнуться на одну вакансию дважды 
- Вакансию можно создать только для своей компании
- По умолчанию показываются только активные вакансии


## Возможные апгрейды:

- Кеширование
- Улучшенная аналитика откликов
- Оптимизация ORM
- Профили для юзеров
- Docker


## Автор

Pet-project для практики DRF и подготовки к backend-собеседованиям. jlxinn
![Python](https://img.shields.io/badge/python-3.11-blue)
![Django](https://img.shields.io/badge/django-5.2-green)
![Coverage](https://img.shields.io/badge/coverage-89%25-brightgreen)
