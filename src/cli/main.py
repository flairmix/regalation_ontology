import typer
from pathlib import Path
from src.ontology.builder import OntologyBuilder
from src.ontology.visualizer import visualize
from src.ontology.base_ontology import create_base_ontology
from src.requirements.graph_builder import load_base_ontology, add_requirement_from_model
from src.requirements.model import Requirement

app = typer.Typer(help="CLI-интерфейс для построения и визуализации строительной онтологии.")

@app.command()
def build_base(
    owl_output: str = "ontology_base.owl",
    html_output: str = "ontology_base.html",
    base_uri: str = "http://example.org/ontology#"
):
    """Создать базовую строительную онтологию (без индивидуумов)."""
    ob = create_base_ontology(base_uri=base_uri)
    ob.save(owl_output)
    classes, properties, individuals = ob.get_entities()
    visualize(classes, properties, individuals, filename=html_output)

@app.command()
def add_requirement(
    json_file: Path = typer.Argument(..., help="Путь к JSON-файлу с описанием требования"),
    base_owl_path: Path = Path("ontology_base.owl")
):
    """Добавить требование на основе JSON в базовую онтологию и сохранить его отдельно."""
    import json
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    req = Requirement.model_validate(data)

    ob = load_base_ontology(str(base_owl_path))

    # Восстановим классы и свойства из загруженной онтологии
    for cls in ob.onto.classes():
        ob.classes[cls.name] = cls
    for prop in ob.onto.object_properties():
        ob.object_properties[prop.name] = prop

    # Собираем все упомянутые классы
    used_classes = [obj.class_name for obj in req.objects]
    used_classes += [p.name for obj in req.objects for p in (obj.properties or [])]
    used_classes += [p.unit for obj in req.objects for p in (obj.properties or []) if p.unit]
    used_classes += [check.type for check in req.checks]
    used_classes += [check.unit for check in req.checks if check.unit]

    for class_name in used_classes:
        if class_name and class_name not in ob.classes:
            raise KeyError(f"Класс '{class_name}' не найден в базе онтологии. Убедитесь, что он был добавлен в build-base.")

    add_requirement_from_model(ob, req)

    output_dir = json_file.parent
    owl_path = output_dir / f"requirement_{req.id}.owl"
    html_path = output_dir / f"requirement_{req.id}.html"

    ob.save(str(owl_path))
    classes, props, inds = ob.get_entities()
    visualize(classes, props, inds, filename=str(html_path))

    typer.echo(f"✅ Требование сохранено:\n- {owl_path}\n- {html_path}")

if __name__ == "__main__":
    app()