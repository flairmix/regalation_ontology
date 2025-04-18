# ONTOLOGY_BUILDER

**Онтология элементов строительства на Python: RDF/OWL, визуализация графов, CLI-интерфейс и тесты.**

[![Test status](https://img.shields.io/badge/tests-passing-brightgreen)](#-тестирование)
[![UV](https://img.shields.io/badge/built%20with-uv-blueviolet)](https://github.com/astral-sh/uv)
[![License](https://img.shields.io/github/license/your-org/ontology_builder)](LICENSE)


📌 Проект включает в себя:
- создание базовой строительной онтологии (OWL)
- добавление требований из JSON
- визуализацию графа через PyVis
- CLI-интерфейс с `typer`
- автоматические тесты через `pytest`
- поддержку `uv` + `pyproject.toml`

---

## 🚀 Быстрый старт

### 📦 Установка зависимостей

```bash
uv venv .venv
uv pip install -r requirements.lock.txt
```

Если файла `requirements.lock.txt` ещё нет:

```bash
uv pip compile pyproject.toml > requirements.lock.txt
uv pip install -r requirements.lock.txt
```

📌 Используется [uv](https://github.com/astral-sh/uv) — ультрабыстрый Python-менеджер.

---

## 🧰 CLI-команды

Все команды запускаются через `uv run`:

```bash
# 📘 Создание базовой онтологии (OWL + HTML)
uv run python -m src.cli.main build-base

# 📦 Добавление требования из JSON
uv run python -m src.cli.main add-requirement src/requirements/data/requirement_R002.json
```

Файлы сохраняются в `src/requirements/data/` как `requirement_XXX.owl` и `requirement_XXX.html`.

---

## 🧪 Тестирование

```bash
uv run pytest tests -v
```

или через `.bat`-файл:

```bash
run_tests.bat
```

Покрываются команды `build-base` и `add-requirement` с проверкой файлов.

---

## 📁 Структура проекта

```
.
├── src/
│   ├── cli/               # CLI-интерфейс (typer)
│   ├── ontology/          # Логика построения онтологии, визуализация
│   ├── requirements/      # Модели требований, генерация графа
│   └── config/, db/       # Под расширение: настройки, графовые БД
│
├── tests/                 # pytest-совместимые тесты
├── pyproject.toml         # Все зависимости
├── requirements.lock.txt  # Зафиксированные версии
├── run_tests.bat          # Автозапуск тестов (Windows)
```

---

## 🔧 Зависимости

| Библиотека                                         | Назначение                         |
| -------------------------------------------------- | ---------------------------------- |
| [`owlready2`](https://pypi.org/project/Owlready2/) | Работа с OWL/RDF и онтологиями     |
| [`pyvis`](https://pyvis.readthedocs.io/)           | Визуализация графов                |
| [`typer`](https://typer.tiangolo.com/)             | Современный CLI-интерфейс          |
| [`pydantic`](https://docs.pydantic.dev/)           | Валидация входных JSON-моделей     |
| [`pytest`](https://docs.pytest.org/)               | Автотесты                          |
| [`uv`](https://github.com/astral-sh/uv)            | Быстрая установка пакетов и `venv` |

---

## 📄 Пример входного требования (JSON)

```json
{
  "id": "R002",
  "objects": [
    { "id": "apartment_1", 
        "class_name": "Apartment", 
        "relations": [{ "property_name": "hasPart", "target": "door_1" }] },
    { "id": "door_1", 
        "class_name": "Door", 
        "relations": [{ "property_name": "hasPart", "target": "door_leaf_1" }] },
    { "id": "door_leaf_1", 
        "class_name": "Door_leaf", 
        "properties": [{ "name": "Width" }] }
  ],
  "conditions": [{ "type": "Condition_component_exist", "target": "door_1" }],
  "checks": [{ 
    "type": "Check_property_value_greater", 
    "target": "door_leaf_1", 
    "unit": "Millimeter", 
    "value": 800.0 }]
}
```

---

## 📬 Контакты

**Flair Team**  
🌐 [flairbim.com](https://flairbim.com)  
📧 [info@flairbim.com](mailto:info@flairbim.com)


