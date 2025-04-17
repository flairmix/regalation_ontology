ontology_project/
├── pyproject.toml
├── README.md
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py              # настройки путей, БД и параметров визуализации
│   ├── ontology/
│   │   ├── __init__.py
│   │   ├── builder.py               # класс OntologyBuilder (перенесённый)
│   │   ├── visualizer.py            # логика визуализации (опционально)
│   │   └── serializer.py            # сохранение в OWL/RDF/XML, импорт из файлов
│   ├── requirements/
│   │   ├── __init__.py
│   │   ├── model.py                 # модель требований
│   │   ├── graph_builder.py         # построение графа по требованию
│   │   └── exporter.py              # экспорт RDF-графа по требованию
│   ├── db/
│   │   ├── __init__.py
│   │   ├── neo4j_connector.py       # подключение к графовой БД
│   │   └── ontology_writer.py       # запись графов и узлов в БД
│   └── cli/
│       ├── __init__.py
│       └── main.py                  # интерфейс запуска через CLI
