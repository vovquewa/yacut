# yacut
Сервис по укорачиванию ссылок

## Автор
[Владимир Козлов](https://github.com/vovquewa/)

## Стек технологий
python 3.7.3
flask 2.0.2


## Развертывание 

Клонировать репозиторий и перейти в него в командной строке:

```bash
git clone git@github.com:vovquewa/yacut.git
```

```bash
cd yacut
```

Cоздать и активировать виртуальное окружение:

```bash
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```bash
    source venv/bin/activate
    ```

* Если у вас windows

    ```bash
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```

## Команды запуска

```bash
python flask run
```

## Справка

```bash
flask --help
```

```bash
Usage: flask [OPTIONS] COMMAND [ARGS]...

  A general utility script for Flask applications.

  Provides commands from Flask, extensions, and the application. Loads the
  application defined in the FLASK_APP environment variable, or from a wsgi.py
  file. Setting the FLASK_ENV environment variable to 'development' will
  enable debug mode.

    $ export FLASK_APP=hello.py
    $ export FLASK_ENV=development
    $ flask run

Options:
  --version  Show the flask version
  --help     Show this message and exit.

Commands:
  db      Perform database migrations.
  routes  Show the routes for the app.
  run     Run a development server.
  shell   Run a shell in the app context.
```
