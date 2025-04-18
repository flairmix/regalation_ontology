@echo off
echo Running ontology tests...

REM 1. Создание виртуального окружения, если ещё не создано
if not exist .venv (
    echo [INFO] Creating .venv using uv...
    uv venv .venv
)

REM 2. Активация окружения
call .venv\Scripts\activate
where python

REM 3. Установка зависимостей из pyproject.toml
if not exist requirements.lock.txt (
    echo [INFO] Compiling dependencies from pyproject.toml...
    uv pip compile pyproject.toml > requirements.lock.txt
)

uv pip install -r requirements.lock.txt

REM 4. Запуск тестов
pytest tests --maxfail=1 --disable-warnings -v

pause
