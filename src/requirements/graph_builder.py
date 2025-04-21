import logging
from owlready2 import get_ontology
from src.ontology.builder import OntologyBuilder
from src.requirements.model import Requirement

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
            prop_ind = ob.add_individual(prop.name, f"{obj.id}_{prop.name.lower()}")
            ob.relate_individuals(instance, "property", prop_ind)
            
            instance_map[f"{obj.id}_{prop.name.lower()}"] = prop_ind

    validation_node = ob.add_individual("Validation", f"Validation{req.id}")

    for condition in req.conditions:
        logger.info(f"Adding condition {condition.type}")
        condition_node = ob.add_individual(condition.type, f"condition_{req.id}_{condition.type.lower()}")
        if condition.target in instance_map:
            ob.relate_individuals(condition_node, "exist", instance_map[condition.target])
            ob.relate_individuals(validation_node, "check", condition_node)

        else:
            raise KeyError(f"Condition target '{condition.target}' not found in instance map.")
        # TODO: добавить обработку условий

    for check in req.checks:
        logger.info(f"Adding check {check.type} for requirement {req.id}")
        check_node = ob.add_individual(check.type, f"check_{req.id}_{check.type.lower()}")

        if check.target in instance_map:
            ob.relate_individuals(check_node, "check", instance_map[check.target])
            ob.relate_individuals(validation_node, "check", check_node)
        else:
            raise KeyError(f"Check target '{check.target}' not found in instance map.")
        
        ob.add_data_property("expectedValue", domain=check.type, dtype=float)
        ob.assign_data_property(check_node, "expectedValue", check.value)
   
        # Единицу измерения тоже можно как DataProperty
        if check.unit:
            ob.add_data_property("unit", domain=check.type, dtype=str)
            ob.assign_data_property(check_node, "unit", check.unit)
            

    for obj in req.objects:
        logger.info(f"Adding relations for object {obj.id}")
        for rel in obj.relations or []:
            if rel.target in instance_map:
                ob.relate_individuals(instance_map[obj.id], rel.property_name, instance_map[rel.target])