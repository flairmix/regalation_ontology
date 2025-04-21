from src.ontology.builder import OntologyBuilder
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # или DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

def create_base_ontology(base_uri="http://example.org/ontology#"):
    ob = OntologyBuilder(base_uri=base_uri)

    # Abstract classes
    Site = ob.add_class("Site")
    Construction = ob.add_class("Construction", parent_class=Site)
    Level = ob.add_class("Level", parent_class=Construction)
    Room = ob.add_class("Room", parent_class=Level)
    Zone = ob.add_class("Zone", parent_class=Level)
    Component = ob.add_class("Component", parent_class=Level)
    Property = ob.add_class("Property")
    Units = ob.add_class("Units")
    Literal = ob.add_class("Literal")

    # Classes
    Apartment = ob.add_class("Apartment", parent_class=Zone)
    Door = ob.add_class("Door", parent_class=Component)
    Window = ob.add_class("Window", parent_class=Component)

    # Subclasses
    Door_leaf = ob.add_class("Door_leaf", parent_class=Door)

    # Properties
    Type_Function = ob.add_class("Type_Function", parent_class=Property)
    Width = ob.add_class("Width", parent_class=Property)
    Height = ob.add_class("Height", parent_class=Property)
    Distance = ob.add_class("Distance", parent_class=Property)

    # Units
    Millimeter = ob.add_class("Millimeter", parent_class=Units)

    # # Relationships
    ob.add_object_property("hasPart", "Component", "Component")
    # ob.add_object_property("hasPart", "Door", "Door_leaf")
    # ob.add_object_property("property", "Door_leaf", "Width")
    # ob.add_object_property("value", "Width", "Millimeter")
    # ob.add_object_property("value", "Height", "Millimeter")
    # ob.add_object_property("value", "Condition", "Millimeter")

    # Validation structure
    Validation = ob.add_class("Validation")

    # Conditions
    Condition = ob.add_class("Condition", parent_class=Validation)
    Condition_component_exist = ob.add_class("Condition_component_exist", parent_class=Condition)
    Condition_property_value_equal = ob.add_class("Condition_property_value_equal", parent_class=Condition)

    # Checks
    Check = ob.add_class("Check", parent_class=Validation)
    Check_property_value_equal = ob.add_class("Check_property_value_equal", parent_class=Check)
    Check_property_value_greater = ob.add_class("Check_property_value_greater", parent_class=Check)
    Check_property_value_less = ob.add_class("Check_property_value_less", parent_class=Check)

    # Validation relationships
    ob.add_object_property("exist", "Condition", "Component")
    ob.add_object_property("check", "Check", "Component")

    try:
        logger.info("Base ontology created successfully.")
        logger.info(f"- number of classes: {len(list(ob.onto.classes()))}")
        logger.info(f"- number of properties: {len(list(ob.onto.object_properties()))}")    
        logger.info(f"- number of individuals: {len(list(ob.onto.individuals()))}")
        logger.info(f"- number of data properties: {len(list(ob.onto.data_properties()))}")
    except Exception() as e:
        logger.error(f"Error creating base ontology: {e}")
    
    return ob
