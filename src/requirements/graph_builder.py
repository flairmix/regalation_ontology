# src/requirements/graph_builder.py

from owlready2 import get_ontology
from src.ontology.builder import OntologyBuilder
from src.requirements.model import Requirement, ObjectInstance, PropertyEntry


def load_base_ontology(path: str) -> OntologyBuilder:
    onto = get_ontology(str(path)).load()
    ob = OntologyBuilder(base_uri=onto.base_iri)
    ob.onto = onto
    return ob


def add_requirement_example(ob: OntologyBuilder, req_id: str = "001") -> None:
    leaf = ob.add_individual("Door_leaf", f"door_leaf_{req_id}")
    width = ob.add_individual("Width", f"width_{req_id}")
    value = ob.add_individual("Millimeter", f"val_{req_id}_mm")
    check = ob.add_individual("Check_property_value_greater", f"check_{req_id}")

    ob.relate_individuals(leaf, "property", width)
    ob.relate_individuals(width, "value", value)
    ob.relate_individuals(check, "check", value)


def add_requirement_from_model(ob: OntologyBuilder, req: Requirement) -> None:
    instance_map = {}

    for obj in req.objects:
        instance = ob.add_individual(obj.class_name, obj.id)
        instance_map[obj.id] = instance

        for prop in obj.properties or []:
            prop_ind = ob.add_individual(prop.name, f"{prop.name.lower()}_{obj.id}")
            ob.relate_individuals(instance, "property", prop_ind)

            if prop.unit:
                val_ind = ob.add_individual(prop.unit, f"val_{obj.id}_{prop.name.lower()}_{prop.unit.lower()}")
                ob.relate_individuals(prop_ind, "value", val_ind)
                # value можно позже оформить через data property или аннотацию

    for obj in req.objects:
        for rel in obj.relations or []:
            if rel.target in instance_map:
                ob.relate_individuals(instance_map[obj.id], rel.property_name, instance_map[rel.target])

    for check in req.checks:
        check_node = ob.add_individual(check.type, f"check_{req.id}_{check.type.lower()}")
        if check.unit:
            val_node = ob.add_individual(check.unit, f"checkval_{req.id}_{check.type.lower()}_{check.unit.lower()}")
            ob.relate_individuals(check_node, "check", val_node)
