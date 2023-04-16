### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com:Alexandrsgit/api_yamdb.git
```

```
cd api_yamdb/

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/Script/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:
...
python manage.py runserver
```
