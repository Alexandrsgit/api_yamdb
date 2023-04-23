### YaMDb ###
Проект YaMDb собирает отзывы пользователей на различные произведения.

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com:Alexandrsgit/api_yamdb.git
cd api_yamdb/
```


Cоздать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Script/activate
```


Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```


Выполнить миграции:
```
python manage.py migrate
```


Запустить проект:
```
python manage.py runserver
```

### Алгоритм регистрации пользователей: ###
Пользователь отправляет POST-запрос на добавление нового пользователя с параметрами email и username на эндпоинт /api/v1/auth/signup/.
YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на адрес email.
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему приходит токен.
При желании пользователь отправляет PATCH-запрос на эндпоинт /api/v1/users/me/ и заполняет поля в своём профайле.