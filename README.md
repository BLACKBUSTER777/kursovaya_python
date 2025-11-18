# kursovaya_python
# Программа с неподвижной точкой (Fixed Point Logic)


Что программа делает фактически

При запуске GUI (`python -m app.gui_app`)
открывается окно с полем ввода, двумя кнопками и областью вывода.
При нажатии «Выполнить программу» приложение читает свой код и печатает его.
При нажатии «Запустить в Docker» оно собирает образ, запускает CLI-версию внутри контейнера и выводит результат.

При запуске CLI (`python -m app.cli`)
программа выводит собственный исходный код, независимо от аргументов командной строки.

При сборке Docker-образа
(команда `docker build -t fixed_quine_app` .)
создаётся контейнер, который при запуске (`docker run --rm fixed_quine_app`) делает то же самое:
выводит свой исходный код.

Pytest-тесты
проверяют, что TinyLang работает корректно и что программа действительно выводит собственный текст.

## Структура
- `cli.py` — Консольная версия (для Docker).
- `gui_app.py` — GUI на PySide6.
- `quine_core.py` — Чтение исходника, формирование f(P).
- `tinylang.py` —  Интерпретатор TinyLang.
- `test_tinylang.py` —  тесты.

## Установка
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Запуск GUI
```bash
python -m app.gui_app
```

## запуск тестов и Docker
```bash
docker build --platform linux/amd64 -t fixedpoint-app . # Собрать образ
docker run --rm -it -v "%cd%\app\app_logs.db:/app/app/app_logs.db" fixedpoint-app "Текст Пользователя"
python -m pytest -v #запуск тестов 
```
