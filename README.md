# Referral system
RESTful API сервис для реферальной системы.

1. Регистрация и аутентификация пользователя (JWT, Oauth 2.0)
2. Аутентифицированный пользователь имеет возможность создать или удалить свой реферальный код.
    Одновременно может быть активен только 1 код.
    При создании кода обязательно должен быть задан его срок годности;
3. Возможность получения реферального кода по email адресу реферера;
4. Возможность регистрации по реферальному коду в 	качестве реферала;
5. Получение информации о рефералах по id  реферера;
6. Получение информации о рефералах по id  реферера;
7. UI документация ReDoc.

## Разверните репозиторий на своем серевере.

1. Клонируйте репозиторий:
```
git clone https://github.com/pitbul892/Referral_system.git
```
2. Создайте и активируйте виртуальное окружения:
```
py -m venv venv
source venv/bin/activate
```
3. Установите зависимости:
```
pip install -r requirements.txt
```
4. Примените миграции:
```
py manage.py migrate
py manage.py runserver
```
5. Создайте суперпользователя:
```
py manage.py createsuperuser
```
6. Запустите сервер разработки:
```
py manage.py runserver
```
Приложение будет доступно по адресу: ```http://127.0.0.1:8000/```
На странице ```http://127.0.0.1:8000/redoc/``` можно ознаомиться с документацией.
# API Эндпоинты
## Аутентификация
Используется пакет Djoser для аутентификации с JWT.

POST  ```/auth/users/```: Регистрация пользователя.

POST ```/auth/jwt/create/```: Получение JWT токена.

POST ```/auth/jwt/refresh/```: Обновление JWT токена.

## Реферальные коды

POST ```/api/referral-code/```: Создать реферальный код.

DELETE ```/api/referral-code/```: Удалить реферальный код.

## Регистрация по реферальному коду

POST ```/api/register-with-referral/```: Регистрация с реферальным кодом.

## Получение списка рефералов

GET ```/api/referrals/{id}/```: Получение списка рефералов по ID реферера.

## Отправка реферального кода на email

GET ```/api/referral-code/email/```: Отправка реферального кода на email реферера.

сообщения отправляются в файл sent_emails. Для отпарвки реальных сообщений можно использовать SMTP backend.