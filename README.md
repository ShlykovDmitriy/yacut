

# **YaCut - сервис по укорачиванию ссылок** 

## Описание
___
Доает возможность создать укороченую ссылку самостоятельно  и автоматически, так же есть подключение по API
___
## Технологии
___
-  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) 
- ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)



___
## Установка и запуск
___
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:ShlykovDmitriy/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать файл .env
```
FLASK_APP=yacut
FLASK_ENV=development
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=YOUR_SECRET_KEY
```

Запустить приложение.
```
flask run
```


___
### Автор
___
[Шлыков Дмитрий](https://github.com/ShlykovDmitriy)