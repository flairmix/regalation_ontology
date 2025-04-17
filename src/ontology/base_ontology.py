# src/ontology/base_ontology.py

from src.ontology.builder import OntologyBuilder

def create_base_ontology(base_uri="http://example.org/ontology#"):
    ob = OntologyBuilder(base_uri=base_uri)

    # Abstract classes
    Site = ob.add_class("Site")
    Construction = ob.add_class("Construction", parent_class=Site)
    Level = ob.add_class("Level", parent_class=Construction)
    Room = ob.add_class("Room", parent_class=Level)
    Zone = ob.add_class("Zone", parent_class=Level)
    Component = ob.add_class("Component")
    Property = ob.add_class("Property")
    Units = ob.add_class("Units")

    # Classes
    Apartment = ob.add_class("Apartment", parent_class=Zone)
    Door = ob.add_class("Door", parent_class=Component)

    # Subclasses
    Door_leaf = ob.add_class("Door_leaf", parent_class=Door)

    # Properties
    Width = ob.add_class("Width", parent_class=Property)
    Height = ob.add_class("Height", parent_class=Property)
    Distance = ob.add_class("Distance", parent_class=Property)

    # Units
    Millimeter = ob.add_class("Millimeter", parent_class=Units)

    # Relationships
    ob.add_object_property("hasPart", "Apartment", "Door")
    ob.add_object_property("hasPart", "Door", "Door_leaf")
    ob.add_object_property("property", "Door_leaf", "Width")
    ob.add_object_property("value", "Width", "Millimeter")
    ob.add_object_property("value", "Height", "Millimeter")
    ob.add_object_property("value", "Condition", "Millimeter")

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
    ob.add_object_property("exist", "Condition_component_exist", "Door")
    ob.add_object_property("check", "Check_property_value_greater", "Millimeter")

    return ob
