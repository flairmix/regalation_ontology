# src/requirements/graph_builder.py

import logging
from owlready2 import get_ontology
from src.ontology.builder import OntologyBuilder
from src.requirements.model import Requirement, ObjectInstance, PropertyEntry

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # или DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def load_base_ontology(path: str) -> OntologyBuilder:
    onto = get_ontology(str(path)).load()
    ob = OntologyBuilder(base_uri=onto.base_iri)
    ob.onto = onto
    return ob


def add_requirement_from_model(ob: OntologyBuilder, req: Requirement) -> None:
    instance_map = {}
    logger.info(f"Adding requirement {req.id} with objects {[obj.id for obj in req.objects]}")

    for obj in req.objects:
        logger.info(f"Adding object {obj.id} of class {obj.class_name}")
        instance = ob.add_individual(obj.class_name, obj.id)
        instance_map[obj.id] = instance

        for prop in obj.properties or []:
            prop_ind = ob.add_individual(prop.name, f"{prop.name.lower()}_{obj.id}")
            ob.relate_individuals(instance, "property", prop_ind)

            if prop.unit:
                val_ind = ob.add_individual(prop.unit, f"val_{obj.id}_{prop.name.lower()}_{prop.unit.lower()}")
                ob.relate_individuals(prop_ind, "value", val_ind)
                # value можно позже оформить через data property или аннотацию


    for condition in req.conditions:
        logger.info(f"Adding condition {condition.type}")
        condition_node = ob.add_individual(condition.type, f"condition_{req.id}_{condition.type.lower()}")
        if condition.target in instance_map:
            ob.relate_individuals(condition_node, "exist", instance_map[condition.target])
        else:
            raise KeyError(f"Condition target '{condition.target}' not found in instance map.")
        # TODO: добавить обработку условий

    for check in req.checks:
        logger.info(f"Adding check {check.type} for requirement {req.id}")
        check_node = ob.add_individual(check.type, f"check_{req.id}_{check.type.lower()}")
        if check.unit:
            val_node = ob.add_individual(check.unit, f"checkval_{req.id}_{check.type.lower()}_{check.unit.lower()}")
            ob.relate_individuals(check_node, "check", val_node)

    for obj in req.objects:
        logger.info(f"Adding relations for object {obj.id}")
        for rel in obj.relations or []:
            if rel.target in instance_map:
                ob.relate_individuals(instance_map[obj.id], rel.property_name, instance_map[rel.target])